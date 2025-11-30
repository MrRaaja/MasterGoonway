# john_pork.py

import random
import datetime
import asyncio

import discord
from discord.ext import commands, tasks

from config import CHANNEL_ID, ACHIEVEMENTS
from data_manager import ensure_user, save_data

QUIET_START = 2   # 02:00 UTC
QUIET_END   = 8   # 08:00 UTC

pork_times_today = []


def setup_john_pork(bot: commands.Bot, data: dict):

    # ------------------------------------------------------------
    # Generate call times
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
    # Trigger Pork call
    # ------------------------------------------------------------
    async def _trigger_pork_if_due():
        now_utc = datetime.datetime.utcnow().strftime("%H:%M")

        if now_utc in pork_times_today:
            pork_times_today.remove(now_utc)

            channel = bot.get_channel(CHANNEL_ID)
            if channel:
                await channel.send(
                    "📞🐖 **John Pork is calling…**\nWho will answer? @everyone",
                    view=view,
                    allowed_mentions=AllowedMentions(everyone=True)
                )

    # ------------------------------------------------------------
    # Award achievement
    # ------------------------------------------------------------
    async def handle_pork_answer(ctx):
        user = str(ctx.author.id)
        ensure_user(data, user)

        if "friend_of_pork" not in data[user]["achievements"]:
            data[user]["achievements"].append("friend_of_pork")
            save_data(data)
            await ctx.send(
                "🐷💖 **You answered John Pork.**\n"
                "🏅 Achievement unlocked: **Friend of Pork**"
            )
        else:
            await ctx.send("🐷📞 John Pork: *Bro we already besties… chill.*")

    # ------------------------------------------------------------------
    # === TASKS (do NOT start them here!) ===
    # ------------------------------------------------------------------
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

    @tasks.loop(minutes=1)
    async def monitor_pork_times():
        await _trigger_pork_if_due()

    # ------------------------------------------------------------
    # Commands
    # ------------------------------------------------------------
    @bot.command(name="pork")
    async def pork_cmd(ctx):
        await handle_pork_answer(ctx)

    @bot.command(name="porktimes")
    async def porktimes_cmd(ctx):
        if not pork_times_today:
            return await ctx.send("📭 **No Pork calls scheduled today yet.**")

        msg = "🐖📅 **Today's John Pork Call Times:**\n"
        for t in pork_times_today:
            msg += f"• 🕒 {t} UTC\n"
        await ctx.send(msg)

    # ------------------------------------------------------------
    # EXPORT TASKS — bot.py will start them in on_ready()
    # ------------------------------------------------------------
    setup_john_pork.generate_daily_pork_times = generate_daily_pork_times
    setup_john_pork.monitor_pork_times = monitor_pork_times
