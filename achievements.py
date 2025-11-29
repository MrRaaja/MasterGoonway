# achievements.py

import random
from config import ACHIEVEMENTS, RARITY_COLORS

def roll_random_achievements(data, user_id: str):
    unlocked = []

    for ach_id, info in ACHIEVEMENTS.items():
        chance = info.get("chance", 0.0)
        if chance <= 0:
            continue

        if ach_id in data[user_id]["achievements"]:
            continue

        if random.random() < chance:
            data[user_id]["achievements"].append(ach_id)
            unlocked.append(ach_id)

    return unlocked

def format_achievement_list(ids):
    lines = []
    for a in ids:
        info = ACHIEVEMENTS[a]
        icon = RARITY_COLORS.get(info["rarity"], "🏅")
        name = info["name"]
        desc = info.get("description", "") 

        if desc:
            lines.append(f"{icon} **{name}**\n🔸 _{desc}_")
        else:
            lines.append(f"{icon} **{name}**")

    return "\n\n".join(lines)
