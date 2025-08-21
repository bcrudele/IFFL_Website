import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os 
import json

def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def update_playerdata_json(skater_data, goalie_data, json_path="playerdata.json"):
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            player_data = json.load(f)
    else:
        player_data = {}

    for row in skater_data:
        full_name = row.get("Player", "").strip()
        if not full_name:
            continue
        parts = full_name.split()
        name = parts[0] + parts[1][0] if len(parts) > 1 else parts[0]
        if not name:
            continue

        team_year = "2025"
        skater_stats = {
            "GP": safe_int(row.get("GP")),
            "G": safe_int(row.get("Goals")),
            "A": safe_int(row.get("Assists")),
            "P": safe_int(row.get("Points")),
            "PPG": safe_float(row.get("PPG")),
            "HT": safe_int(row.get("HT")),
        }

        player_data.setdefault(name, {}).setdefault(team_year, {})["skater"] = skater_stats

    for row in goalie_data:
        full_name = row.get("Player", "").strip()
        if not full_name:
            continue
        parts = full_name.split()
        name = parts[0] + parts[1][0] if len(parts) > 1 else parts[0]

        if not name:
            continue

        team_year = "2025"
        saves = safe_int(row.get("Saves"))
        ga = safe_int(row.get("GA"))
        goalie_stats = {
            "GP": safe_int(row.get("GP")),
            "SV": saves,
            "SVPercent": safe_float(row.get("SV%")),
            "GA": ga,
            "GAA": safe_float(row.get("GAA")),
            "SA": safe_int(row.get("Shots")) if "Shots" in row else saves + ga,
            "W": safe_int(row.get("Wins")),
        }

        player_data.setdefault(name, {}).setdefault(team_year, {})["goalie"] = goalie_stats

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(player_data, f, indent=2)

    print(f"Updated {json_path} with current stats.")



# Setup Google Sheets client
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

button_names = {
    "CHI": "button-list-charge",
    "DUN": "button-list-charge",
    "ALG": "button-list-alg",
    "TAL": "button-list",
}

def update_skater_html(team_name, sheet_id, data, html_file, html_content):
    block_pattern = r'(<div class="button-container-list">.*?<button class="title-button">.*?Name.*?Points.*?</button>)(.*?)(</div>)'
    matches = re.finditer(block_pattern, html_content, flags=re.DOTALL)

    updated_blocks = []

    for match in matches:
        header, old_rows, footer = match.groups()
        new_rows = ""
        for row in data:
            if team_name not in row.get("Team", "").split("/"):
                continue

            player_name = row.get("Player", "-")
            if player_name != "-":
                filename = "/pages/players/" + player_name.lower().replace(" ", "_") + ".html"
                onclick_attr = f'onclick="location.href=\'{filename}\'"'
            else:
                onclick_attr = ""

            new_rows += (
                f'                       <button class="{button_names[team_name]}" {onclick_attr}>\n'
                f'                          <span>{player_name}</span>\n'
                f'                          <span>-</span>\n'
                f'                          <span>{row.get("GP", "-")}</span>\n'
                f'                          <span>{row.get("Goals", "-")}</span>\n'
                f'                          <span>{row.get("Assists", "-")}</span>\n'
                f'                          <span>{row.get("Points", "-")}</span>\n'
                '                       </button>\n'
            )
        updated_blocks.append((match.span(), f"{header}\n{new_rows}{footer}"))

    for span, new_block in reversed(updated_blocks):
        html_content = html_content[:span[0]] + new_block + html_content[span[1]:]

    print(f"Updated skater stats for {team_name} in {sheet_id}")
    return html_content

def update_goalie_html(team_name, sheet_id, data, html_file, html_content):
    block_pattern = r'(<div class="button-container-list" id="goalies">.*?<button class="title-button">.*?GAA.*?</button>)(.*?)(</div>)'
    match = re.search(block_pattern, html_content, flags=re.DOTALL)

    if not match:
        print(f"No goalie block found in {html_file}")
        return html_content

    header, old_rows, footer = match.groups()
    new_rows = ""
    for row in data:
        if team_name not in row.get("Team", "").split("/"):
            continue
        player_name = row.get("Player", "-")
        if player_name != "-":
            filename = "/pages/players/" + player_name.lower().replace(" ", "_") + ".html"
            onclick_attr = f'onclick="location.href=\'{filename}\'"'
        else:
            onclick_attr = ""


        new_rows += (
            f'                        <button class="{button_names[team_name]}" {onclick_attr}>\n'
            f'                          <span>{player_name}</span>\n'
            f'                          <span>{row.get("GP", "-")}</span>\n'
            f'                          <span>{row.get("Saves", "-")}</span>\n'
            f'                          <span>{row.get("SV%", "-")}</span>\n'
            f'                          <span>{row.get("GA", "-")}</span>\n'
            f'                          <span>{row.get("GAA", "-")}</span>\n'
            '                       </button>\n'
        )

    new_block = f"{header}\n{new_rows}{footer}"
    html_content = html_content[:match.start()] + new_block + html_content[match.end():]

    print(f"Updated goalie stats for {team_name} in {sheet_id}")
    return html_content

# Configuration
SPREADSHEET_ID = "1Wa1Rae5O8IiWuSOXl-DCfPDmRCC4fK8Kri9v56qmPOc"
sheet_html_mapping = {
    "Stats (Skaters)": [
        {"html_file": "pages/charge.html"},
        {"html_file": "pages/assassins.html"},
        {"html_file": "pages/demons.html"},
        {"html_file": "pages/turtles.html"}
    ],
    "Stats (Goalies)": [
        {"html_file": "pages/charge.html"},
        {"html_file": "pages/assassins.html"},
        {"html_file": "pages/demons.html"},
        {"html_file": "pages/turtles.html"}
    ]
}

def team_loader():

    # Main execution loop
    skater_entries = sheet_html_mapping["Stats (Skaters)"]
    goalie_entries = sheet_html_mapping["Stats (Goalies)"]

    skater_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Stats (Skaters)")
    goalie_sheet = client.open_by_key(SPREADSHEET_ID).worksheet("Stats (Goalies)")

    skater_data = skater_sheet.get_all_records()
    goalie_data = goalie_sheet.get_all_records()

    for skater_entry, goalie_entry in zip(skater_entries, goalie_entries):
        html_file = skater_entry["html_file"]
        with open(html_file, "r", encoding="utf-8") as file:
            html_content = file.read()

        if html_file == "pages/charge.html":
            team_name = "CHI"
        elif html_file == "pages/assassins.html":
            team_name = "ALG"
        elif html_file == "pages/demons.html":
            team_name = "DUN"
        elif html_file == "pages/turtles.html":
            team_name = "TAL"
        # team_name = input(f"Enter team name for {html_file}: ").strip()

        html_content = update_skater_html(team_name, "Stats (Skaters)", skater_data, html_file, html_content)
        html_content = update_goalie_html(team_name, "Stats (Goalies)", goalie_data, html_file, html_content)
        update_playerdata_json(skater_data, goalie_data)

        with open(html_file, "w", encoding="utf-8") as file:
            file.write(html_content)

    print("✅ Team HTML files updated successfully.")
