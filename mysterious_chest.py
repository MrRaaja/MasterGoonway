# mysterious_chest.py

import random
import asyncio

import discord
from discord.ext import tasks, commands

from data_manager import ensure_user, save_data
from config import CHANNEL_ID, ESSENCE_NAME, ACHIEVEMENTS

OWNER_ID = "475968988002779156"

chest_state = {
    "active": False,
    "resolved": False,
    "message": None,
    "winner": None,
}


def setup_mysterious_chest(bot: commands.Bot, data: dict):

    async def award_achievement(user_id: str, achievement_key: str):
        """Give an achievement if user does not already have it."""
        ensure_user(data, user_id)
        if achievement_key not in data[user_id]["achievements"]:
            data[user_id]["achievements"].append(achievement_key)
            return ACHIEVEMENTS[achievement_key]["name"]
        return None

    async def start_chest_event(channel: discord.TextChannel):
        """Spawn a single Mysterious Chest event in the given channel."""
        if chest_state["active"]:
            await channel.send("💼 A Mysterious Chest is already here. Handle that one first.")
            return

        chest_state["active"] = True
        chest_state["resolved"] = False
        chest_state["winner"] = None
        chest_state["message"] = None

        # Buttons
        open_button = discord.ui.Button(
            label="Open Carefully",
            style=discord.ButtonStyle.success
        )
        kick_button = discord.ui.Button(
            label="Kick It",
            style=discord.ButtonStyle.danger
        )
        run_button = discord.ui.Button(
            label="Run Away",
            style=discord.ButtonStyle.secondary
        )

        async def resolve_once(inter: discord.Interaction, action: str):
            if chest_state["resolved"]:
                return await inter.response.send_message(
                    "Too late, the chest has already been dealt with.",
                    ephemeral=True
                )

            uid = str(inter.user.id)
            chest_state["resolved"] = True
            chest_state["winner"] = uid

            ensure_user(data, uid)

            xp_gain = 0
            essence_delta = 0
            result_text = ""
            achievement_unlocked = None

            # --- OPEN CAREFULLY ---
            if action == "open":
                if random.random() < 0.5:  # GOOD
                    xp_gain = 120
                    result_text = (
                        "✨ You gently open the chest and discover **glowing loot**!\n"
                        f"🎯 You gain **{xp_gain} XP**."
                    )
                    achievement_unlocked = await award_achievement(uid, "chest_luck_blessed")

                else:  # TRAP
                    xp_gain = 10
                    essence_delta = -5
                    result_text = (
                        "💥 A hidden trap explodes!\n"
                        f"🎯 You gain **{xp_gain} XP**, but spill **5 ml** of {ESSENCE_NAME}."
                    )
                    achievement_unlocked = await award_achievement(uid, "chest_luck_cursed")

            # --- KICK IT ---
            elif action == "kick":
                if random.random() < 0.4:  # GOOD-ish
                    xp_gain = 80
                    result_text = (
                        "🦵 You kick the chest open with reckless style!\n"
                        f"🎯 You gain **{xp_gain} XP**."
                    )
                else:
                    xp_gain = 10
                    essence_delta = -2
                    result_text = (
                        "📉 You kick the chest and hurt your foot.\n"
                        f"🎯 You gain **{xp_gain} XP**, but lose **2 ml** of {ESSENCE_NAME}."
                    )

                achievement_unlocked = await award_achievement(uid, "reckless_chest_kicker")

            # --- RUN AWAY ---
            elif action == "run":
                xp_gain = 5
                result_text = (
                    "🏃‍♂️ You flee from the mysterious chest.\n"
                    f"🎯 You gain **{xp_gain} XP** for survival instincts."
                )
                achievement_unlocked = await award_achievement(uid, "cowardly_escape_artist")

            # Apply XP
            data[uid]["xp"] += xp_gain

            # Apply Essence delta
            if essence_delta != 0:
                jar = data["_jar"]
                jar["total_ml"] = max(0, jar.get("total_ml", 0) + essence_delta)

            save_data(data)

            # Private response
            ach_text = f"\n🏅 Achievement unlocked: **{achievement_unlocked}**" if achievement_unlocked else ""

            await inter.response.send_message(
                f"💼 **You interacted with the Mysterious Chest!**\n"
                f"{result_text}{ach_text}",
                ephemeral=True
            )

            # Public announcement
            await channel.send(
                f"💼 **The Mysterious Chest has been resolved!**\n"
                f"🏅 <@{uid}> chose **{action.upper()}**.\n"
                f"{result_text}{ach_text}"
            )

            chest_state["active"] = False

        # Button bindings
        open_button.callback = lambda inter: resolve_once(inter, "open")
        kick_button.callback = lambda inter: resolve_once(inter, "kick")
        run_button.callback = lambda inter: resolve_once(inter, "run")

        view = discord.ui.View()
        view.add_item(open_button)
        view.add_item(kick_button)
        view.add_item(run_button)

        chest_state["message"] = await channel.send(
            "💼 **A Mysterious Chest Appears...**\n"
            "Only one gooner may choose its fate.\n"
            "What will you do?",
            view=view
        )

    # EXPOSE start function
    setup_mysterious_chest.start_event = start_chest_event

    # MANUAL command
    @bot.command(name="chest")
    async def chest_cmd(ctx: commands.Context):
        if str(ctx.author.id) != OWNER_ID:
            return await ctx.send("⛔ Only the Master Goon may summon the Mysterious Chest.")
        await start_chest_event(ctx.channel)

    # AUTO scheduler every 3 hours
    @tasks.loop(hours=3)
    async def chest_scheduler():
        channel = bot.get_channel(CHANNEL_ID)
        if not channel:
            return

        if chest_state["active"]:
            return

        await asyncio.sleep(random.randint(0, 59) * 60 + random.randint(0, 59))

        if not chest_state["active"]:
            await start_chest_event(channel)

    setup_mysterious_chest.scheduler = chest_scheduler
