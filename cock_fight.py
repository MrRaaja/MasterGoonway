# cock_fight.py

import time
import asyncio
import random

import discord
from discord.ext import commands, tasks
from discord import AllowedMentions

from data_manager import ensure_user, save_data
from config import ACHIEVEMENTS, CHANNEL_ID

# Only YOU can start manually
OWNER_ID = "475968988002779156"

# Shared global state
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

# ============================================================
# Main Setup Entry
# ============================================================
def setup_cock_fight(bot: commands.Bot, data: dict):

    # ============================================================
    # Status animation
    # ============================================================
    async def render_status() -> str:
        if len(cock_state["players"]) < 2:
            return "Waiting for two brave fighters..."

        p1, p2 = cock_state["players"]
        h1 = cock_state["hits"].get(p1, 0)
        h2 = cock_state["hits"].get(p2, 0)

        bar1 = "💦" * min(h1, 20)
        bar2 = "💦" * min(h2, 20)

        remaining = max(0.0, cock_state["end_time"] - time.monotonic())

        return (
            "💦 **COCK SMASHING BATTLE — LIVE 🍆**\n"
            f"<@{p1}>: {bar1 or '…'} ({h1} hits)\n"
            f"<@{p2}>: {bar2 or '…'} ({h2} hits)\n\n"
            f"⏳ Time left: **{remaining:.1f}s**"
        )

    # ============================================================
    # Duel Loop
    # ============================================================
    async def duel_loop(channel: discord.TextChannel):
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

            # Final update
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

    # ============================================================
    # Finish Duel
    # ============================================================
    async def finish_duel(channel: discord.TextChannel):
        if not cock_state["active"]:
            return

        cock_state["active"] = False

        if len(cock_state["players"]) < 2:
            await channel.send("Duel ended — not enough fighters joined.")
            return

        p1, p2 = cock_state["players"]
        h1 = cock_state["hits"][p1]
        h2 = cock_state["hits"][p2]

        if h1 > h2:
            winner = p1
        elif h2 > h1:
            winner = p2
        else:
            await channel.send("🤝 **Tie!** Both fighters smashed equally.")
            return

        # XP + achievement
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

    # ============================================================
    # Ready Phase
    # ============================================================
    async def send_ready_prompt(channel):
        ready_button = discord.ui.Button(
            label="Ready",
            style=discord.ButtonStyle.success
        )

        async def ready_callback(inter):
            await inter.response.defer(ephemeral=True)
            uid = str(inter.user.id)

            if uid not in cock_state["players"]:
                return await inter.followup.send(
                    "You are not part of this duel.",
                    ephemeral=True
                )

            cock_state["ready"].add(uid)
            await inter.followup.send("✅ Ready!", ephemeral=True)

            if len(cock_state["ready"]) == 2:
                await channel.send("🔥💦 Both fighters ready! Starting in **3… 2… 1…**")
                await start_fight(channel)

        ready_button.callback = ready_callback

        view = discord.ui.View()
        view.add_item(ready_button)

        await channel.send(
            "👊 Both fighters joined.\n"
            "Click **Ready** to start.\n",
            view=view
        )

    # ============================================================
    # Start Fight
    # ============================================================
    async def start_fight(channel):
        hit_button = discord.ui.Button(
            label="HIT!",
            style=discord.ButtonStyle.danger
        )

        async def hit_callback(inter):
            uid = str(inter.user.id)

            if uid not in cock_state["players"]:
                return await inter.response.send_message(
                    "You are not in this duel.",
                    ephemeral=True
                )

            if time.monotonic() > cock_state["end_time"]:
                return await inter.response.send_message(
                    "Duel already ended.",
                    ephemeral=True
                )

            cock_state["hits"][uid] += 1
            await inter.response.defer()

        hit_button.callback = hit_callback

        view = discord.ui.View()
        view.add_item(hit_button)

        cock_state["end_time"] = time.monotonic() + 10

        msg = await channel.send(
            "🔥 **COCK SMASHING BATTLE — LIVE 🐓💦**\n"
            "Mash **HIT!** for **10 seconds**!",
            view=view
        )
        cock_state["fight_message"] = msg

        if not cock_state["loop_running"]:
            bot.loop.create_task(duel_loop(channel))

    # ============================================================
    # Start Event (manual or automatic)
    # ============================================================
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

        join_button = discord.ui.Button(
            label="Join Fight",
            style=discord.ButtonStyle.primary
        )

        async def join_callback(inter):
            await inter.response.defer(ephemeral=True)
            uid = str(inter.user.id)

            if uid in cock_state["players"]:
                return await inter.followup.send(
                    "You already joined.",
                    ephemeral=True
                )

            if len(cock_state["players"]) >= 2:
                return await inter.followup.send(
                    "Two fighters already joined.",
                    ephemeral=True
                )

            cock_state["players"].append(uid)
            cock_state["hits"][uid] = 0

            await inter.followup.send(
                f"⚔️ {inter.user.name} entered the arena!",
                ephemeral=True
            )

            if len(cock_state["players"]) == 2:
                await send_ready_prompt(channel)

        join_button.callback = join_callback

        view = discord.ui.View()
        view.add_item(join_button)

        await channel.send(
            "@everyone 🥵 **Beat The Cock – Two fighters needed!**\n"
            "Press **Join Fight** to enter.",
            view=view,
            allowed_mentions=AllowedMentions(everyone=True)
        )

    # ============================================================
    # Manual owner-only command
    # ============================================================
    @bot.command(name="cockfight")
    async def cockfight_cmd(ctx):
        if str(ctx.author.id) != OWNER_ID:
            return await ctx.send("⛔ Only the Master Goon may summon a Cock Battle.")
        await start_cock_event(ctx.channel)

    # ============================================================
    # Automatic 4× per day (every 6 hours)
    # ============================================================
    @tasks.loop(hours=6)
    async def auto_cockfight():
        channel = bot.get_channel(CHANNEL_ID)
        if not channel:
            return

        if cock_state["active"]:
            return

        # Random delay inside the 6h block
        await asyncio.sleep(random.randint(0, 59) * 60)
        await asyncio.sleep(random.randint(0, 59))

        await channel.send(
            "@everyone 🍆 **A Wild Cock Battle Has Appeared!**\n"
            "Who’s brave enough to smash first?",
            allowed_mentions=AllowedMentions(everyone=True)
        )

        await start_cock_event(channel)

    # Make auto_cockfight accessible to bot.py
    setup_cock_fight.auto_cockfight = auto_cockfight
