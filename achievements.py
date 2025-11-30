# achievements.py

import random
from config import ACHIEVEMENTS, RARITY_COLORS, RARITY_PRIORITY


def roll_random_achievements(data, user_id: str):
    """
    Rolls for ALL random achievements but awards ONLY ONE (the rarest).
    """

    rolled = []

    for ach_id, info in ACHIEVEMENTS.items():
        chance = info.get("chance", 0.0)

        # skip non-random achievements
        if chance <= 0:
            continue

        # skip if already unlocked
        if ach_id in data[user_id]["achievements"]:
            continue

        # RNG roll
        if random.random() < chance:
            rolled.append(ach_id)

    # No wins
    if not rolled:
        return []

    # Pick the rarest one based on config-defined priority
    rolled.sort(
        key=lambda a: RARITY_PRIORITY[ACHIEVEMENTS[a]["rarity"]],
        reverse=True
    )

    winner = rolled[0]

    # Add final achievement
    data[user_id]["achievements"].append(winner)

    return [winner]  # always list with 1 item


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
