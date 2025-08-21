import json
import re
import os

# ==== Globals ====
players_dir = "pages\\players"
completed_players = set()

# ==== Utility Functions ====

def progress_bars(filename):
    player_name = os.path.splitext(os.path.basename(filename))[0]
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    updated = update_progress_bars(content, player_name)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(updated)

def update_progress_bars(html, player_name):
    pattern = re.compile(
        r'(\(<td id="[^"]+">(\d+)</td>/(\d+)\)</p>\s*<div[^>]*>\s*<div[^>]*?style="[^"]*?width:\s*)(\d+)%([^"]*?)(")',
        flags=re.DOTALL
    )
    def repl(match):
        current = int(match.group(2))
        total = int(match.group(3))
        percent = min(max(int((current / total) * 100), 1), 100)
        if percent == 100:
            completed_players.add(player_name)
        return f'{match.group(1)}{percent}%{match.group(5)}{match.group(6)}'
    return pattern.sub(repl, html)

def completed_stage():
    if completed_players:
        print("\n🎯 Players with 100% achievement progress:")
        for player in sorted(completed_players):
            print(f"  ✔ {player.replace('_', ' ').title()}")
    else:
        print("\nNo players reached 100% progress.")

def mod_td_values(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html = file.read()

    pattern = re.compile(r'\(<td([^>]*)>(\d+)</td>/(\d+)\)')
    def replacer(match):
        td_attrs = match.group(1)
        num = int(match.group(2))
        den = int(match.group(3))
        mod = num % den
        return f'(<td{td_attrs}>{mod}</td>/{den})'

    updated_html = pattern.sub(replacer, html)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_html)

def apply_stats_to_html(player_key, stats, file_map):
    filename = file_map.get(player_key, player_key.lower())
    html_path = os.path.join(players_dir, f"{filename}.html")

    if not os.path.exists(html_path):
        print(f"❌Skipping {player_key}: {html_path} not found.")
        return

    with open(html_path, encoding="utf-8") as f:
        html = f.read()

    for year, categories in stats.items():
        for role, values in categories.items():
            for stat, value in values.items():
                tag_id = f'{player_key}_{year}_{role}_{stat}'
                pattern = fr'(<td id="{tag_id}">)(.*?)(</td>)'
                html = re.sub(pattern, lambda m: f'{m.group(1)}{value}{m.group(3)}', html)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    progress_bars(html_path)
    print(f"Updated {player_key}'s profile.")

def apply_mod_and_progress(file_map):
    for player_key in completed_players:
        filename = file_map.get(player_key, player_key.lower())
        html_path = os.path.join(players_dir, f"{filename}.html")
        if os.path.exists(html_path):
            #mod_td_values(html_path)
            progress_bars(html_path)
            print(f"Applied modulo and progress updates to {player_key}'s profile.")
    completed_players.clear()

# ==== Step 1: Load and Compute Career Totals ====
def profile_loader():
    with open("playerdata.json", encoding="utf-8") as f:
        data = json.load(f)

    for player, seasons in data.items():
        skater_totals = {"G": 0, "A": 0, "P": 0, "HT": 0}
        goalie_totals = {"W": 0, "SA": 0, "SV": 0, "GA": 0}
        total_skater_gp = total_goalie_gp = 0

        for year, year_data in seasons.items():
            if year == "career":
                continue

            skater = year_data.get("skater", {})
            goalie = year_data.get("goalie", {})

            if year == "2025":
                sv_count = goalie.get("SV", 0)
                a_count = skater.get("A", 0)

                if "achievements" not in data[player][year]:
                    data[player][year]["achievements"] = {}
                data[player][year]["achievements"]["2025_SAVESURGE"] = sv_count
                data[player][year]["achievements"]["2025_BIGAPPLES"] = a_count

            total_skater_gp += skater.get("GP", 0)
            total_goalie_gp += goalie.get("GP", 0)

            skater_totals["G"] += skater.get("G", 0)
            skater_totals["A"] += skater.get("A", 0)
            skater_totals["P"] += skater.get("P", 0)
            skater_totals["HT"] += skater.get("HT", 0)

            goalie_totals["W"] += goalie.get("W", 0)
            goalie_totals["SA"] += goalie.get("SA", 0)
            goalie_totals["SV"] += goalie.get("SV", 0)
            goalie_totals["GA"] += goalie.get("GA", 0)

        skater_totals["GP"] = total_skater_gp
        skater_totals["PPG"] = round(skater_totals["P"] / total_skater_gp, 2) if total_skater_gp else 0

        goalie_totals["GP"] = total_goalie_gp
        goalie_totals["GAA"] = round(goalie_totals["GA"] / total_goalie_gp, 2) if total_goalie_gp else 0
        goalie_totals["SVPercent"] = round(goalie_totals["SV"] / goalie_totals["SA"], 3) if goalie_totals["SA"] else 0

        existing_achievements = data[player].get("career", {}).get("achievements", {})

        data[player]["career"] = {
            "skater": skater_totals,
            "goalie": goalie_totals,
            "achievements": existing_achievements
        }

    with open("playerdata.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("✅ Updated career totals in playerdata.json")

    # ==== Step 2: Apply Stats to HTML ====

    with open("playerdata.json", encoding="utf-8") as f:
        stats = json.load(f)

    player_file_map = {
        "AidanN": "aidan_newett",
        "AnthonyW": "anthony_woodcock",
        "BrandonB": "brandon_bagneschi",
        "BrandonC": "brandon_crudele",
        "ChandlerR": "chandler_rogaskie",
        "CodyC": "cody_christensen",
        "ColinY": "colin_young",
        "DavidD": "david_delatorre",
        "DeanR": "dean_rizzo",
        "DylanG": "dylan_gunter",
        "GrahamH": "graham_holmes",
        "HunterS": "hunter_schiefelbein",
        "JacobW": "jacob_weber",
        "JamesL": "james_lundell",
        "JaredP": "jared_petrin",
        "JimmyD": "jimmy_doles",
        "JustinM": "justin_massillo",
        "KarlK": "karl_koleczek",
        "MikeyD": "mikey_duval",
        "RyanK": "ryan_konecki",
        "SamA": "sam_andrade",
        "SeanM": "sean_mau",
        "TeddyB": "teddy_bittman",
        "TommyL": "tommy_lykowski",
        "TonyM": "tony_mitchell",
        "TylerW": "tyler_wibbeler",
        "MattM": "matt_miedema"
    }

    for player_key in stats:
        apply_stats_to_html(player_key, stats[player_key], player_file_map)
        

    completed_stage()
    apply_mod_and_progress(player_file_map)
