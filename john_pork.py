# john_pork.py

import random
import datetime
import asyncio

import discord
from discord.ext import commands, tasks
from discord import AllowedMentions

from config import CHANNEL_ID, ACHIEVEMENTS
from data_manager import ensure_user, save_data

# Only the owner can manually summon Pork
OWNER_ID = "475968988002779156"

# Quiet hours (no calls)
QUIET_START = 2   # 02:00 UTC
QUIET_END   = 8   # 08:00 UTC

# Storage for today’s Pork call times
pork_times_today = []


def setup_john_pork(bot: commands.Bot, data: dict):

    # ------------------------------------------------------------
    # Generate three call times outside quiet hours
    # ------------------------------------------------------------
    def _generate_pork_times():
        times = []
        while len(times) < 3:
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)

            if QUIET_START <= hour < QUIET_END:
                continue

            times.append(f"{hour:02d}:{minute:02d}")

        return sorted(times)

    # ------------------------------------------------------------
    # Send actual John Pork message
    # ------------------------------------------------------------
    async def send_john_pork_message(channel):

        # Load image safely
        try:
            file = discord.File("assets/john_pork.webp", filename="john_pork.webp")
        except Exception as e:
            print("ERROR loading John Pork image:", e)
            file = None

        # Create Answer button
        answer_button = discord.ui.Button(
            label="Answer Call",
            style=discord.ButtonStyle.success
        )

        async def callback(inter):
            await handle_pork_answer(inter)

        answer_button.callback = callback

        view = discord.ui.View()
        view.add_item(answer_button)

        # Send Pork call
        await channel.send(
            content="@everyone 📞🐖 **John Pork is calling…**\nWho will answer?",
            file=file,
            view=view,
            allowed_mentions=AllowedMentions(everyone=True)
        )

    # ------------------------------------------------------------
    # Check if it's time for Pork to call
    # ------------------------------------------------------------
    async def _trigger_pork_if_due():
        now_utc = datetime.datetime.utcnow().strftime("%H:%M")

        if now_utc in pork_times_today:
            pork_times_today.remove(now_utc)

            channel = bot.get_channel(CHANNEL_ID)
            if channel:
                await send_john_pork_message(channel)

    # ------------------------------------------------------------
    # Handle a user answering the call
    # ------------------------------------------------------------
    async def handle_pork_answer(ctx):
        user = str(ctx.user.id) if hasattr(ctx, "user") else str(ctx.author.id)

        ensure_user(data, user)

        # Give XP
        data[user]["xp"] += 70

        # Award only once
        if "friend_of_pork" not in data[user]["achievements"]:
            data[user]["achievements"].append("friend_of_pork")
            save_data(data)

            await ctx.response.send_message(
                "🐷💖 **You answered John Pork!**\n"
                "🏅 Achievement unlocked: **Friend of Pork**\n"
                "✨ Reward: **+70 XP**",
                ephemeral=False
            )
        else:
            await ctx.response.send_message(
                "🐷📞 John Pork: *Bro we already besties… chill.*",
                ephemeral=True
            )

    # ------------------------------------------------------------
    # Daily reset at midnight UTC
    # ------------------------------------------------------------
    @tasks.loop(time=datetime.time(hour=0, minute=0, tzinfo=datetime.timezone.utc))
    async def generate_daily_pork_times():
        global pork_times_today

        pork_times_today = _generate_pork_times()

        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            msg = "🐖📅 **Today's John Pork Call Times:**\n"
            for t in pork_times_today:
                msg += f"• 🕒 {t} UTC\n"
            await channel.send(msg)

    # ------------------------------------------------------------
    # Check every minute for Pork call
    # ------------------------------------------------------------
    @tasks.loop(minutes=1)
    async def monitor_pork_times():
        await _trigger_pork_if_due()

    # ------------------------------------------------------------
    # Commands
    # ------------------------------------------------------------

    # Manual summon — ONLY OWNER
    @bot.command(name="pork")
    async def pork_cmd(ctx):
        if str(ctx.author.id) != OWNER_ID:
            return await ctx.send("⛔ Only the Master Goon may summon John Pork.")

        channel = ctx.channel
        await send_john_pork_message(channel)

    # Show times
    @bot.command(name="porktimes")
    async def porktimes_cmd(ctx):
        if not pork_times_today:
            return await ctx.send("📭 **No Pork calls scheduled today yet.**")

        msg = "🐖📅 **Today's John Pork Call Times:**\n"
        for t in pork_times_today:
            msg += f"• 🕒 {t} UTC\n"
        await ctx.send(msg)

    # ------------------------------------------------------------
    # Export tasks to bot.py
    # ------------------------------------------------------------
    setup_john_pork.generate_daily_pork_times = generate_daily_pork_times
    setup_john_pork.monitor_pork_times = monitor_pork_times
