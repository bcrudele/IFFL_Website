# can generate HTML achievement with gradients and denominators.
import json

# holds achievement tiers if bronze or better:
results = []

with open("playerdata.json", "r", encoding="utf-8") as f:
    data = json.load(f)
# Map JSON keys to actual HTML filenames
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

achievement_tiers = {
    "SAVESURGE": {"BASIC": 0, "BRONZE": 150, "SILVER": 300, "GOLD": 500},
    "FORTRESS": {"BASIC": 0, "BRONZE": 3, "SILVER": 5, "GOLD": 7},
    "DUELIST": {"BASIC": 0, "BRONZE": 1, "SILVER": 3, "GOLD": 7},
    "BIGAPPLES": {"BASIC": 0, "BRONZE": 10, "SILVER": 20, "GOLD": 40},
    "HOTHAND": {"BASIC": 0, "BRONZE": 3, "SILVER": 5, "GOLD": 7},
    "CAREERSCORER": {"BASIC": 0, "BRONZE": 25, "SILVER": 50, "GOLD": 100},
    "PLAYMAKER": {"BASIC": 0, "BRONZE": 15, "SILVER": 30, "GOLD": 60},
    "HATTRICK": {"BASIC": 0, "BRONZE": 3, "SILVER": 10, "GOLD": 20},
    "BRICKBYBRICK": {"BASIC": 0, "BRONZE": 5, "SILVER": 10, "GOLD": 15},
    "UNDERSIEGE": {"BASIC": 0, "BRONZE": 250, "SILVER": 500, "GOLD": 1000},
    "WALLOFSTEEL": {"BASIC": 0, "BRONZE": 1, "SILVER": 3, "GOLD": 5},
}

# Map tier → progress bar gradient
tier_colors = {
    "BASIC": "linear-gradient(90deg, #cd7f32, #b87333);",
    "BRONZE": "linear-gradient(90deg, #c0c0c0, #dcdcdc)",
    "SILVER": "linear-gradient(90deg, #ffd700, #f9a602)",
    "GOLD": "linear-gradient(90deg, #ffd700, #f9a602)",
}

templates = {
    "SAVESURGE": """
<div style="margin-bottom: 20px;">
  <h4 style="margin: 0;">🌊 2025 Save Surge</h4>
  <p style="margin: 4px 0; color: #555;">Make {denominator} saves (<td id="{tag}_2025_achievements_2025_SAVESURGE">{statline}</td>/{denominator})</p>
  <div style="background: #eee; border-radius: 8px;">
    <div style="width: {perc}%; background: {bar_color}; height: 16px; border-radius: 8px;"></div>
  </div>
</div>
""",
    "FORTRESS": """
<div style="margin-bottom: 20px;">
  <h4 style="margin: 0;">🏰 2025 Fortress</h4>
  <p style="margin: 4px 0; color: #555;">0.800+ SV% in {denominator} games (<td id="{tag}_2025_achievements_2025_FORTRESS">{statline}</td>/{denominator})</p>
  <div style="background: #eee; border-radius: 8px;">
    <div style="width: {perc}%; background: {bar_color}; height: 16px; border-radius: 8px;"></div>
  </div>
</div>
""",
    "DUELIST": """
<div style="margin-bottom: 20px;">
  <h4 style="margin: 0;">⚔️ 2025 Duelist</h4>
  <p style="margin: 4px 0; color: #555;">Win {denominator} rival matchups (<td id="{tag}_2025_achievements_2025_DUELIST">{statline}</td>/{denominator})</p>
  <div style="background: #eee; border-radius: 8px;">
    <div style="width: {perc}%; background: {bar_color}; height: 16px; border-radius: 8px;"></div>
  </div>
</div>
""",
    "BIGAPPLES": """
<div style="margin-bottom: 20px;">
  <h4 style="margin: 0;">🍎 2025 Big Apples</h4>
  <p style="margin: 4px 0; color: #555;">Hit {denominator} assists (<td id="{tag}_2025_achievements_2025_BIGAPPLES">{statline}</td>/{denominator})</p>
  <div style="background: #eee; border-radius: 8px;">
    <div style="width: {perc}%; background: {bar_color}; height: 16px; border-radius: 8px;"></div>
  </div>
</div>
""",
    "HOTHAND": """
<div style="margin-bottom: 20px;">
  <h4 style="margin: 0;">🔥 2025 Hot Hand</h4>
  <p style="margin: 4px 0; color: #555;">Points in {denominator} consecutive games (<td id="{tag}_2025_achievements_2025_HOTHAND">{statline}</td>/{denominator})</p>
  <div style="background: #eee; border-radius: 8px;">
    <div style="width: {perc}%; background: {bar_color}; height: 16px; border-radius: 8px;"></div>
  </div>
</div>
""",
"BRICKBYBRICK": """
<div style="margin-bottom: 20px;">
  <h4 style="margin: 0;">🧱 Brick by Brick</h4>
  <p style="margin: 4px 0; color: #555;">Make 30+ saves in a single game (<td id="{tag}_career_achievements_BRICKBYBRICK">{statline}</td>/{denominator})</p>
  <div style="background: #eee; border-radius: 8px;">
    <div style="width: {perc}%; background: {bar_color}; height: 16px; border-radius: 8px;"></div>
  </div>
</div>
""",

"UNDERSIEGE": '''
<div style="margin-bottom: 20px;">
  <h4 style="margin: 0;">⛑️ Under Siege</h4>
  <p style="margin: 4px 0; color: #555;">Face {denominator} shots (<td id="{tag}_career_goalie_SA">{statline}</td>/{denominator})</p>
  <div style="background: #eee; border-radius: 8px;">
    <div style="width: {perc}%; background: {bar_color}; height: 16px; border-radius: 8px;"></div>
  </div>
</div>
''', 

"WALLOFSTEEL": '''
<div style="margin-bottom: 20px;">
  <h4 style="margin: 0;">🛡️ Wall of Steel</h4>
  <p style="margin: 4px 0; color: #555;">Hold an opponent to 3 goals or fewer (<td id="{tag}_career_achievements_WALLOFSTEEL">{statline}</td>/{denominator})</p>
  <div style="background: #eee; border-radius: 8px;">
    <div style="width: {perc}%; background: {bar_color}; height: 16px; border-radius: 8px;"></div>
  </div>
</div>
''',
    "CAREERSCORER": '''
    <div style="margin-bottom: 20px;">
    <h4 style="margin: 0;">🎯 Career Scorer</h4>
    <p style="margin: 4px 0; color: #555;">{denominator} career goals (<td id="{tag}_career_skater_G">{statline}</td>/{denominator})</p>
    <div style="background: #eee; border-radius: 8px;">
        <div style="width: {perc}%; background: {bar_color}; height: 16px; border-radius: 8px;"></div>
    </div>
    </div>
    ''',

    "PLAYMAKER": '''
    <div style="margin-bottom: 20px;">
    <h4 style="margin: 0;">🧠 The Playmaker</h4>
    <p style="margin: 4px 0; color: #555;">{denominator} career assists (<td id="{tag}_career_skater_A">{statline}</td>/{denominator})</p>
    <div style="background: #eee; border-radius: 8px;">
        <div style="width: {perc}%; background: {bar_color}; height: 16px; border-radius: 8px;"></div>
    </div>
    </div>
    ''',

    "HATTRICK": '''
    <div>
    <h4 style="margin: 0;">🎩 Hat Trick Hero</h4>
    <p style="margin: 4px 0; color: #555;">{denominator} career hat tricks (<td id="{tag}_career_skater_HT">{statline}</td>/{denominator})</p>
    <div style="background: #eee; border-radius: 8px;">
        <div style="width: {perc}%; background: {bar_color}; height: 16px; border-radius: 8px;"></div>
    </div>
    </div>
    '''
}

def get_highest_tier(player_data: dict, achievement: str) -> str:
    """
    Determine the highest tier a player qualifies for for a specific achievement.
    """
    achievement = achievement.upper()
    tiers = achievement_tiers.get(achievement, {})
    value = None

    # Determine stat source
    if achievement == "SAVESURGE":
        value = player_data.get("2025", {}).get("achievements", {}).get("2025_SAVESURGE", 0)
    elif achievement == "FORTRESS":
        value = player_data.get("2025", {}).get("achievements", {}).get("2025_FORTRESS", 0)
    elif achievement == "DUELIST":
        value = player_data.get("2025", {}).get("achievements", {}).get("2025_DUELIST", 0)
    elif achievement == "BIGAPPLES":
        value = player_data.get("2025", {}).get("achievements", {}).get("2025_BIGAPPLES", 0)
    elif achievement == "HOTHAND":
        value = player_data.get("2025", {}).get("achievements", {}).get("2025_HOTHAND", 0)
    elif achievement == "BRICKBYBRICK":
        value = player_data.get("career", {}).get("achievements", {}).get("BRICKBYBRICK", 0)
    elif achievement == "UNDERSIEGE":
        value = player_data.get("career", {}).get("goalie", {}).get("SA", 0)
    elif achievement == "WALLOFSTEEL":
        value = player_data.get("career", {}).get("achievements", {}).get("WALLOFSTEEL", 0)
    elif achievement == "CAREERSCORER":
        value = player_data.get("career", {}).get("skater", {}).get("G", 0)
    elif achievement == "PLAYMAKER":
        value = player_data.get("career", {}).get("skater", {}).get("A", 0)
    elif achievement == "HATTRICK":
        value = player_data.get("career", {}).get("skater", {}).get("HT", 0)
    else:
        return "BASIC", None
    # print(f"Achievement: {achievement}, Value: {value}")
    # Evaluate highest tier met
    best_tier = "BASIC"
    for tier in ["GOLD", "SILVER", "BRONZE"]:
        required = tiers.get(tier, float('inf'))
        if value >= required:
            return tier, value
    return best_tier, value


def generate_achievement_html(player_tag: str, achievement: str, player_data: dict) -> str:
    """
    Generate the HTML for the highest-tier achievement for a player.
    """
    achievement = achievement.upper()
    tier, statline = get_highest_tier(player_data, achievement)
    # print(tier)
    if tier not in achievement_tiers[achievement]:
        return f"Invalid tier: {tier} for {achievement}"

    if tier not in tier_colors:
        return f"Missing bar color for tier: {tier}"
    tier_order = ["BASIC", "BRONZE", "SILVER", "GOLD"]
    index = tier_order.index(tier)
    if index + 1 < len(tier_order):
        next_tier = tier_order[index + 1]
        next_denominator = achievement_tiers[achievement][next_tier]
        current_denominator = achievement_tiers[achievement][tier]

        gap = next_denominator - current_denominator
        remainder = statline - current_denominator
        perc = round((remainder / gap) * 100) if gap > 0 else 100
    else:
        next_tier = tier
        next_denominator = achievement_tiers[achievement][tier]

    if index + 1 == len(tier_order):
        perc = 100 # overflow prot.
        
    denominator = achievement_tiers[achievement][tier]
    bar_color = tier_colors[tier]
    # statline = player_data.get("2025", {}).get("achievements", {}).get(f"2025_{achievement}", 0)
    if tier != "BASIC":
        results.append((player_tag, achievement, tier))

    if achievement not in templates:
        return f"No HTML template defined for {achievement}."
    # print(denominator)
    return templates[achievement].format(
        denominator=next_denominator,
        tag=player_tag,
        bar_color=bar_color,
        statline=statline, 
        perc= perc if perc > 0 else 1
    )


# Example test
if __name__ == "__main__":

  player_key = "AnthonyW"
  player_data = data[player_key]

  html = generate_achievement_html(player_key, "PLAYMAKER", player_data)
  print(html)
