from html_replace import html_replacer
from team_loader import team_loader
from profile_loader import profile_loader
from generate_achievement import results

tier_emojis = {
    "BRONZE": "🥉",
    "SILVER": "🥈",
    "GOLD": "🥇"
}

if __name__ == "__main__":
    # Load and update team stats
    team_loader()

    # Load and update player profiles
    profile_loader()

    # Replace HTML content in files
    html_replacer()
    
    print("✅ All updates completed successfully.")

    for player_tag, achievement, tier in results:
        emoji = tier_emojis.get(tier.upper(), "")
        print(f"Player: {player_tag} | Achievement: {achievement} | Tier: {tier} {emoji}")