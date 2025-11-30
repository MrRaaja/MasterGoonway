# cock_fight.py

import time
import asyncio
import random
import datetime

import discord
from discord.ext import commands, tasks
from discord import AllowedMentions

from data_manager import ensure_user, save_data
from config import ACHIEVEMENTS, CHANNEL_ID

OWNER_ID = "475968988002779156"

# Global daily fight schedule
scheduled_fight_times = []

# Duel global state
cock_state = {
    "active": False,
    "players": [],
    "hits": {},
    "message": None,
    "fight_message": None,
    "end_time": 0.0,
    "ready": set(),
    "loop_running": False
}


def setup_cock_fight(bot: commands.Bot, data: dict):

    # ------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------
    async def render_status():
        if len(cock_state["players"]) < 2:
            return "Waiting for two brave fighters..."

        p1, p2 = cock_state["players"]
        h1 = cock_state["hits"].get(p1, 0)
        h2 = cock_state["hits"].get(p2, 0)

        bar1 = "💦" * min(h1, 20)
        bar2 = "💦" * min(h2, 20)

        remaining = max(0, cock_state["end_time"] - time.monotonic())

        return (
            "💦 **COCK SMASHING BATTLE — LIVE 🍆**\n"
            f"<@{p1}>: {bar1 or '…'} ({h1} hits)\n"
            f"<@{p2}>: {bar2 or '…'} ({h2} hits)\n\n"
            f"⏳ Time left: **{remaining:.1f}s**"
        )

    # ------------------------------------------------------------
    async def duel_loop(channel):
        cock_state["loop_running"] = True
        try:
            while cock_state["active"] and time.monotonic() < cock_state["end_time"]:
                if cock_state["fight_message"]:
                    try:
                        await cock_state["fight_message"].edit(
                            content=await render_status()
                        )
                    except:
                        pass
                await asyncio.sleep(0.3)

            if cock_state["fight_message"]:
                try:
                    await cock_state["fight_message"].edit(
                        content=await render_status()
                    )
                except:
                    pass

            await finish_duel(channel)
        finally:
            cock_state["loop_running"] = False

    # ------------------------------------------------------------
    async def finish_duel(channel):
        if not cock_state["active"]:
            return

        cock_state["active"] = False

        if len(cock_state["players"]) < 2:
            return await channel.send("Duel ended — not enough fighters.")

        p1, p2 = cock_state["players"]
        h1 = cock_state["hits"].get(p1, 0)
        h2 = cock_state["hits"].get(p2, 0)

        if h1 == h2:
            return await channel.send("🤝 **Tie!** Both fighters smashed equally.")

        winner = p1 if h1 > h2 else p2

        ensure_user(data, winner)
        data[winner]["xp"] += 50

        if "fastest_gooner_west" not in data[winner]["achievements"]:
            data[winner]["achievements"].append("fastest_gooner_west")

        save_data(data)

        await channel.send(
            f"🏆 **Winner: <@{winner}>**\n"
            f"🔥 Hits: **{cock_state['hits'][winner]}**\n"
            f"🎁 Reward: **+50 XP**\n"
            f"🏅 Achievement: **{ACHIEVEMENTS['fastest_gooner_west']['name']}**"
        )

    # ------------------------------------------------------------
    async def send_ready_prompt(channel):
        btn = discord.ui.Button(label="Ready", style=discord.ButtonStyle.success)

        async def callback(inter):
            await inter.response.defer(ephemeral=True)
            uid = str(inter.user.id)

            if uid not in cock_state["players"]:
                return await inter.followup.send("You are not part of this duel.", ephemeral=True)

            cock_state["ready"].add(uid)
            await inter.followup.send("✅ Ready!", ephemeral=True)

            if len(cock_state["ready"]) == 2:
                await channel.send("🔥💦 Both fighters ready! Starting in 3… 2… 1…")
                await start_fight(channel)

        btn.callback = callback

        view = discord.ui.View()
        view.add_item(btn)

        await channel.send("👊 Both fighters joined.\nClick Ready to start.", view=view)

    # ------------------------------------------------------------
    async def start_fight(channel):
        btn = discord.ui.Button(label="HIT!", style=discord.ButtonStyle.danger)

        async def callback(inter):
            uid = str(inter.user.id)
            if uid not in cock_state["players"]:
                return await inter.response.send_message("You are not in this duel.", ephemeral=True)

            if time.monotonic() > cock_state["end_time"]:
                return await inter.response.send_message("Duel ended.", ephemeral=True)

            cock_state["hits"][uid] += 1
            await inter.response.defer()

        btn.callback = callback

        view = discord.ui.View()
        view.add_item(btn)

        cock_state["end_time"] = time.monotonic() + 10

        msg = await channel.send(
            "🔥 **COCK SMASHING BATTLE — LIVE 🐓💦**\nMash HIT! for 10 seconds!",
            view=view
        )
        cock_state["fight_message"] = msg

        if not cock_state["loop_running"]:
            bot.loop.create_task(duel_loop(channel))

    # ------------------------------------------------------------
    async def start_cock_event(channel):
        global cock_state

        if cock_state["active"]:
            return await channel.send("🍆 A duel is already running!")

        cock_state = {
            "active": True,
            "players": [],
            "hits": {},
            "message": None,
            "fight_message": None,
            "end_time": 0.0,
            "ready": set(),
            "loop_running": False
        }

        btn = discord.ui.Button(label="Join Fight", style=discord.ButtonStyle.primary)

        async def callback(inter):
            await inter.response.defer(ephemeral=True)
            uid = str(inter.user.id)

            if uid in cock_state["players"]:
                return await inter.followup.send("Already joined.", ephemeral=True)

            if len(cock_state["players"]) >= 2:
                return await inter.followup.send("Two fighters already joined.", ephemeral=True)

            cock_state["players"].append(uid)
            cock_state["hits"][uid] = 0

            await inter.followup.send(f"⚔️ {inter.user.name} entered the arena!", ephemeral=True)

            if len(cock_state["players"]) == 2:
                await send_ready_prompt(channel)

        btn.callback = callback

        view = discord.ui.View()
        view.add_item(btn)

        await channel.send(
            "@everyone 🥵 **Beat The Cock – Two fighters needed!**\nPress Join Fight to enter.",
            view=view,
            allowed_mentions=AllowedMentions(everyone=True)
        )

    # ------------------------------------------------------------
    # Manual force start
    # ------------------------------------------------------------
    @bot.command(name="cockfight")
    async def cockfight_cmd(ctx):
        if str(ctx.author.id) != OWNER_ID:
            return await ctx.send("⛔ Only the Master Goon may summon a Cock Battle.")
        await start_cock_event(ctx.channel)

    # ------------------------------------------------------------
    # Scheduling System v2
    # ------------------------------------------------------------
    def _generate_daily_times():
        """Generate 4 random times today, excluding 02:00–08:00 UTC."""
        times = []

        while len(times) < 4:
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)

            # Skip forbidden window
            if 2 <= hour < 8:
                continue

            times.append(f"{hour:02d}:{minute:02d}")

        return sorted(times)


    async def _trigger_fight_if_due():
        if not scheduled_fight_times:
            return

        now_utc = datetime.datetime.utcnow().strftime("%H:%M")

        if now_utc in scheduled_fight_times:
            scheduled_fight_times.remove(now_utc)

            channel = bot.get_channel(CHANNEL_ID)
            if channel:
                await channel.send(
                    "@everyone 🍆 **A Wild Cock Battle Has Appeared!**\n"
                    "Who’s brave enough to smash first?",
                    allowed_mentions=AllowedMentions(everyone=True)
                )
                await start_cock_event(channel)

    @tasks.loop(time=datetime.time(hour=0, minute=0, tzinfo=datetime.timezone.utc))
    async def generate_daily_cock_times():
        global scheduled_fight_times
        scheduled_fight_times = _generate_daily_times()

        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            msg = "📅 **Today's Cock Fight Times:**\n"
            for t in scheduled_fight_times:
                msg += f"• 🕒 {t} UTC\n"
            await channel.send(msg)

    @tasks.loop(minutes=1)
    async def monitor_cock_times():
        await _trigger_fight_if_due()

    @bot.command(name="cocktimes")
    async def cocktimes_cmd(ctx):
        global scheduled_fight_times

        # If the list is empty → generate new times for today
        if not scheduled_fight_times:
            scheduled_fight_times = _generate_daily_times()

            msg = "📅 **Today's Cock Fight Times (Generated Now):**\n"
            for t in scheduled_fight_times:
                msg += f"• 🕒 {t} UTC\n"

            return await ctx.send(msg)

        # If list exists → show it
        msg = "📅 **Today's Cock Fight Times:**\n"
        for t in scheduled_fight_times:
            msg += f"• 🕒 {t} UTC\n"

        await ctx.send(msg)

# ------------------------------------------------------------
# EXPORT tasks to bot.py (do NOT start them here)
# ------------------------------------------------------------

    setup_cock_fight.generate_daily_cock_times = generate_daily_cock_times
    setup_cock_fight.monitor_cock_times = monitor_cock_times
