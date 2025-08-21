import json
import random
from generate_achievement import player_file_map

# Load player data
with open("playerdata.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Build dict of players with valid PPG
ppg_dict = {
    player: data.get(player, {}).get("2025", {}).get("skater", {}).get("PPG", 0)
    for player in player_file_map
    if data.get(player, {}).get("2025", {}).get("skater", {}).get("GP", 0) > 0
}

# Sort by PPG descending
sorted_players = sorted(ppg_dict.items(), key=lambda x: x[1], reverse=True)
eligible_count = len(sorted_players)
print(f"Eligible player count: {eligible_count}")

# Determine number of tiers
tiers = 2
players_per_tier = eligible_count // tiers
leftover = eligible_count % tiers

# Distribute players across tiers evenly
tiered_players = []
start = 0
for i in range(tiers):
    extra = 1 if i < leftover else 0
    end = start + players_per_tier + extra
    tiered_players.append(sorted_players[start:end])
    start = end

# Pair players within each tier
for tier_num, players in enumerate(tiered_players, 1):
    print(f"Tier {tier_num} players: {len(players)}")
    random.shuffle(players)
    
    # If odd, carry forward the unmatched player to the next tier
    if len(players) % 2 != 0 and tier_num < tiers:
        tiered_players[tier_num].append(players.pop())  # move extra to next tier

    for i in range(0, len(players), 2):
        player1, ppg1 = players[i]
        player2, ppg2 = players[i + 1]
        print(f"  Player: {player1}, PPG: {ppg1:.2f} VS Player: {player2}, PPG: {ppg2:.2f}")

# Final unmatched player (if any) gets matched with a random peer
all_assigned = sum(len(tier) for tier in tiered_players)
if all_assigned < eligible_count:
    unassigned = sorted_players[all_assigned:]
    for player in unassigned:
        rival = random.choice(sorted_players)
        print(f"  Player: {player[0]}, PPG: {player[1]:.2f} VS Player: {rival[0]}, PPG: {rival[1]:.2f} (fallback match)")
