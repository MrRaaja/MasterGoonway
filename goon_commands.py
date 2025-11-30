# goon_commands.py

from datetime import datetime
import random
from discord.ext import commands

from config import (
    ESSENCE_NAME,
    BASE_ESSENCE_PER_GOON,
    BASE_XP_PER_GOON,
    JAR_MILESTONES_ML,
    ACHIEVEMENTS
)
from data_manager import ensure_user, ensure_jar, save_data
from cooldowns import get_cooldown_seconds, get_level
from achievements import roll_random_achievements, format_achievement_list

def setup_goon_commands(bot: commands.Bot, data: dict):

    @bot.command()
    async def goon(ctx):
        """Gain XP with dynamic cooldown, sickness, random achievements and fill the jar."""
        user = str(ctx.author.id)
        now = datetime.utcnow().timestamp()

        ensure_user(data, user)
        ensure_jar(data)

        xp = data[user]["xp"]

        # 1) Check sickness
        if now < data[user]["sick_until"]:
            remaining = int(data[user]["sick_until"] - now)
            mins = remaining // 60
            secs = remaining % 60
            return await ctx.send(
                f"🤒 **You are sick and cannot goon right now!**\n"
                f"Try again in **{mins}m {secs}s**."
            )

        # 2) Normal cooldown
        cooldown = get_cooldown_seconds(xp)
        elapsed = now - data[user]["last_goon_time"]

        if elapsed < cooldown:
            remaining = int(cooldown - elapsed)
            mins = remaining // 60
            secs = remaining % 60
            return await ctx.send(
                f"⏳ **Cooldown!** Try again in **{mins}m {secs}s**."
            )

        # 3) Sickness mechanic (3% chance)
        if random.random() < 0.03:
            sick_time = 3600  # 1 hour
            data[user]["sick_until"] = now + sick_time

            if "blue_balls" not in data[user]["achievements"]:
                data[user]["achievements"].append("blue_balls")

            save_data(data)
            return await ctx.send(
                f"🤒 **{ctx.author.name} got SICK!**\n"
                f"You must rest for **1 hour**.\n"
                f"🏅 Achievement unlocked: **Blue Balls**"
            )

        # 4) Bonus based on extra wait time
        extra_time = max(0, elapsed - cooldown)

        if extra_time <= 0:
            multiplier = 1.0
        else:
            max_extra = cooldown * 4  # waiting 5x cooldown -> max
            ratio = min(extra_time / max_extra, 1.0)
            multiplier = 1.0 + 2.0 * ratio  # 1.0 to 3.0

        xp_gain = int(BASE_XP_PER_GOON * multiplier)
        essence_gain = int(BASE_ESSENCE_PER_GOON * multiplier)

        # 5) Successful goon
        data[user]["last_goon_time"] = now
        data[user]["sick_until"] = 0

        data[user]["xp"] += xp_gain
        xp = data[user]["xp"]
        level = get_level(xp)

        # First goon achievement
        if "first_goon" not in data[user]["achievements"]:
            data[user]["achievements"].append("first_goon")

        # 6) Random achievements with rarities
        unlocked_ids = roll_random_achievements(data, user)

        # 7) Update global jar
        jar = data["_jar"]
        old_total = jar.get("total_ml", 0)
        new_total = old_total + essence_gain
        jar["total_ml"] = new_total

        last_milestone = jar.get("last_milestone", 0)
        reached = [m for m in JAR_MILESTONES_ML if last_milestone < m <= new_total]
        if reached:
            jar["last_milestone"] = max(reached)

        save_data(data)

        # Build response
        cd_msg = (
            f"{cooldown} seconds" if cooldown < 60
            else f"{cooldown//60} minutes"
        )

        msg = (
            f"🌀 **{ctx.author.name} is gooning...**\n"
            f"⭐ Level: **{level}**\n"
            f"🎯 XP gained: **{xp_gain}**\n"
            f"💧 Essence this goon: **{essence_gain} ml**\n"
            f"🧪 {ESSENCE_NAME} total: **{new_total} ml** (~{new_total/1000:.2f} L)\n"
            f"⏱ Cooldown: **{cd_msg}**"
        )

        if unlocked_ids:
            msg += "\n\n🎁 **Random Achievements Unlocked!**\n"
            msg += format_achievement_list(unlocked_ids)

        await ctx.send(msg)

        # 8) Announce jar milestones
        if reached:
            for m in reached:
                await ctx.send(
                    f"🎉 **Milestone reached in {ESSENCE_NAME}!**\n"
                    f"Total essence has passed **{m/1000:.0f} L**!"
                )
