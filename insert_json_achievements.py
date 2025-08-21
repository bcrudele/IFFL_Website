import json

def insert_2025_achievements():

    # Load your data here (as a Python dictionary), for example:
    with open('playerdata.json', 'r') as f:
        data = json.load(f)

    for player in data.values():
        if "2025" not in player:
            player["2025"] = {}

        skater_stats = player["2025"]

        # Ensure the 'achievements' sub-dictionary exists
        if "achievements" not in skater_stats:
            skater_stats["achievements"] = {}

        achievements = skater_stats["achievements"]

        # Move or initialize achievement stats into the 'achievements' dictionary
        for key in ["2025_DUELIST", "2025_BIGAPPLES", "2025_HOTHAND", "2025_FORTRESS", "2025_SAVESURGE"]:
            achievements[key] = skater_stats.pop(key, 0)

    # Optionally write the updated data back to a file
    with open('playerdata.json', 'w') as f:
        json.dump(data, f, indent=2)

def insert_career_achievements():

    # Load your data here (as a Python dictionary), for example:
    with open('playerdata.json', 'r') as f:
        data = json.load(f)

    for player in data.values():
        if "career" not in player:
            player["career"] = {}

        skater_stats = player["career"]

        # Ensure the 'achievements' sub-dictionary exists
        if "achievements" not in skater_stats:
            skater_stats["achievements"] = {}

        achievements = skater_stats["achievements"]

        # Move or initialize achievement stats into the 'achievements' dictionary
        for key in ["BRICKBYBRICK", "WALLOFSTEEL"]:
            achievements[key] = skater_stats.pop(key, 0)

    # Optionally write the updated data back to a file
    with open('playerdata.json', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    # insert_2025_achievements()
    # print("Achievements for 2025 inserted successfully.")
    insert_career_achievements()
    print("Career achievements inserted successfully.")