# john_pork.py

import random
import asyncio

import discord
from discord.ext import tasks, commands
from discord import AllowedMentions

from data_manager import ensure_user, save_data
from config import CHANNEL_ID

# Same owner as cock_fight
OWNER_ID = "475968988002779156"

john_state = {
    "active": False,
    "winner": None,
    "message": None
}


def setup_john_pork(bot: commands.Bot, data: dict):

    # =============================
    # Core event logic
    # =============================
    async def start_john_pork_event(channel: discord.TextChannel):
        if john_state["active"]:
            # Optional: tell channel he is already calling
            await channel.send("📞🐷 John Pork is already calling someone...")
            return

        john_state["active"] = True
        john_state["winner"] = None

        button = discord.ui.Button(
            label="Answer John Pork",
            style=discord.ButtonStyle.success
        )

        async def button_callback(inter: discord.Interaction):
            uid = str(inter.user.id)

            # Already answered
            if john_state["winner"] is not None:
                return await inter.response.send_message(
                    "Someone already answered John Pork!",
                    ephemeral=True
                )

            john_state["winner"] = uid

            ensure_user(data, uid)
            # XP reward
            data[uid]["xp"] += 70

            # Achievement: Friend of Pork
            if "friend_of_pork" not in data[uid]["achievements"]:
                data[uid]["achievements"].append("friend_of_pork")

            save_data(data)


            await inter.response.send_message(
                "📞🐷 **John Pork picked up YOUR call!**\n"
                "You earned **+70 XP**.",
                ephemeral=True
            )

            await channel.send(
                f"📞🐷 **John Pork has been answered!**\n"
                f"🏆 Winner: <@{uid}>\n"
                f"🎁 Reward: **+70 XP**"
            )

            john_state["active"] = False

        button.callback = button_callback

        view = discord.ui.View()
        view.add_item(button)

        # Try to send with image, fall back to no image if file missing
        try:
            file = discord.File("assets/john_pork.webp", filename="john_pork.webp")
            msg = await channel.send(
                "📞🐷 **John Pork is calling…**\n"
                "First gooner to press the button answers and wins **70 XP**!",
                file=file,
                view=view
            )
        except Exception:
            msg = await channel.send(
                "📞🐷 **John Pork is calling…**\n"
                "First gooner to press the button answers and wins **70 XP**!",
                view=view
            )

        john_state["message"] = msg

    # Expose for other modules if needed
    setup_john_pork.start_event = start_john_pork_event

    # =============================
    # Manual command
    # =============================
    @bot.command(name="johnpork")
    async def johnpork_cmd(ctx: commands.Context):
        if str(ctx.author.id) != OWNER_ID:
            return await ctx.send("⛔ Only the Master Goon can summon John Pork manually.")
        await start_john_pork_event(ctx.channel)

    # =============================
    # Automatic random every 3 hours
    # =============================
    @tasks.loop(hours=3)
    async def john_pork_scheduler():
        channel = bot.get_channel(CHANNEL_ID)
        if not channel:
            return

        # If an event is already active, skip this slot
        if john_state["active"]:
            return

        # Random delay inside the 3-hour window
        # 0–59 minutes + 0–59 seconds
        await asyncio.sleep(random.randint(0, 59) * 60 + random.randint(0, 59))

        await start_john_pork_event(channel)

    # Make scheduler accessible from bot.py
    setup_john_pork.scheduler = john_pork_scheduler
