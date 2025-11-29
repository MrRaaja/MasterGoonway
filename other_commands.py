# other_commands.py

import random
import discord
from discord.ext import commands
from datetime import datetime, timedelta

from config import ESSENCE_NAME, ACHIEVEMENTS, RARITY_COLORS
from data_manager import load_quotes
from cooldowns import get_level





def setup_other_commands(bot: commands.Bot, data: dict):

    @bot.command()
    async def stats(ctx):
        """Show your XP, level, and achievements with descriptions."""
        user = str(ctx.author.id)
        if user not in data:
            return await ctx.send("You have no stats yet. Use `!goon` first.")

        xp = data[user]["xp"]
        level = get_level(xp)
        ach_ids = data[user]["achievements"]

        if not ach_ids:
            ach_text = "No achievements yet."
        else:
            lines = []
            for a in ach_ids:
                info = ACHIEVEMENTS.get(a)
                if not info:
                    continue

                icon = RARITY_COLORS.get(info["rarity"], "🏅")
                name = info["name"]
                desc = info.get("description", "")

                if desc:
                    lines.append(f"{icon} **{name}**\n🔸 *{desc}*")
                else:
                    lines.append(f"{icon} **{name}**")

            ach_text = "\n\n".join(lines)

        embed = discord.Embed(
            title=f"📜 Journey of {ctx.author.name}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Level", value=level, inline=True)
        embed.add_field(name="XP", value=str(xp), inline=True)
        embed.add_field(name="Achievements", value=ach_text, inline=False)

        await ctx.send(embed=embed)

    @bot.command()
    async def jar(ctx):
        """Show how full the global jar is."""
        jar = data.get("_jar", {"total_ml": 0, "last_milestone": 0})
        total_ml = jar.get("total_ml", 0)
        liters = total_ml / 1000.0

        await ctx.send(
            f"🧪 **{ESSENCE_NAME}**\n"
            f"Total essence: **{total_ml} ml** (~**{liters:.2f} L**)"
        )

    @bot.command()
    async def topgoons(ctx):
        """Show the top gooners by XP."""
        if not data:
            return await ctx.send("No gooners have begun their journey yet.")

        # Filter out special keys
        user_items = [(uid, d) for uid, d in data.items() if not uid.startswith("_")]
        if not user_items:
            return await ctx.send("No gooners have begun their journey yet.")

        sorted_users = sorted(user_items, key=lambda x: x[1]["xp"], reverse=True)
        limit = 10
        lines = []

        for rank, (user_id, stats) in enumerate(sorted_users[:limit], start=1):
            xp = stats["xp"]
            level = get_level(xp)
            member = ctx.guild.get_member(int(user_id))
            if member:
                name = member.display_name
            else:
                try:
                    user_obj = await bot.fetch_user(int(user_id))
                    name = user_obj.name
                except Exception:
                    name = f"User {user_id}"

            if rank == 1:
                medal = "🥇"
            elif rank == 2:
                medal = "🥈"
            elif rank == 3:
                medal = "🥉"
            else:
                medal = f"{rank}."

            lines.append(f"{medal} **{name}** — {xp} XP — *{level}*")

        embed = discord.Embed(
            title="🏆 Top Gooners",
            description="\n".join(lines),
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)

    @bot.command()
    async def quote(ctx):
        """Send a random goon quote manually."""
        quotes = load_quotes()
        if not quotes:
            return await ctx.send("No quotes found in quotes.txt.")
        q = random.choice(quotes)
        await ctx.send(f"🔹 **Goon Quote:**\n{q}")

    @bot.command()
    async def reloadquotes(ctx):
        """Reload quotes from file (admin)."""
        quotes = load_quotes()
        await ctx.send(f"🔄 Reloaded **{len(quotes)}** quotes from file.")

    @bot.command()
    async def nextquote(ctx):
        """Show how long until next daily quote at 00:00."""
        now = datetime.now()
        next_midnight = (now + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        remaining = next_midnight - now
        hours = remaining.seconds // 3600
        minutes = (remaining.seconds % 3600) // 60
        seconds = remaining.seconds % 60

        await ctx.send(
            f"🌙 **Next daily quote at 00:00**\n"
            f"⏳ Time remaining: **{hours}h {minutes}m {seconds}s**"
        )

    @bot.command()
    async def helpme(ctx):
        msg = (
            "**🤖 GoonBot Commands**\n"
            "`!goon` — Gain XP, fill the jar, maybe get sick/loot\n"
            "`!stats` — Your XP, level, achievements\n"
            "`!jar` — Show the global jar volume\n"
            "`!topgoons` — Leaderboard by XP\n"
            "`!quote` — Random goon quote\n"
            "`!nextquote` — Time until next daily quote\n"
            "`!helpme` — This help message\n"
        )
        await ctx.send(msg)

