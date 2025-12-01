# other_commands.py

import random
import discord
from discord.ext import commands
from datetime import datetime, timedelta

from config import ESSENCE_NAME, ACHIEVEMENTS, RARITY_COLORS
from data_manager import load_quotes
from cooldowns import get_level
from discord.ui import View, Button





from discord.ui import View, Button


def setup_other_commands(bot: commands.Bot, data: dict):

    @bot.command()
    async def stats(ctx):
        """Show XP, level, and achievements with pagination."""
        user = str(ctx.author.id)

        if user not in data:
            return await ctx.send("You have no stats yet. Use `!goon` first.")

        xp = data[user]["xp"]
        level = get_level(xp)

        # newest achievements first
        ach_ids = list(reversed(data[user]["achievements"]))

        # ========== PAGE BUILDING ==========
        pages = []
        current = ""

        for ach in ach_ids:
            info = ACHIEVEMENTS.get(ach)
            if not info:
                continue

            icon = RARITY_COLORS.get(info["rarity"], "🏅")
            name = info["name"]
            desc = info.get("description", "")

            block = f"{icon} **{name}**\n🔸 *{desc}*\n\n"

            if len(current) + len(block) > 900:
                pages.append(current)
                current = block
            else:
                current += block

        if current:
            pages.append(current)

        if not pages:
            pages = ["No achievements yet."]

        total_pages = len(pages)

        # ========== EMBED BUILDER ==========
        def make_embed(index):
            embed = discord.Embed(
                title=f"📜 Journey of {ctx.author.display_name}",
                color=discord.Color.blue()
            )
            embed.add_field(name="Level", value=level, inline=True)
            embed.add_field(name="XP", value=str(xp), inline=True)
            embed.add_field(
                name=f"Achievements (Page {index+1}/{total_pages})",
                value=pages[index],
                inline=False
            )
            return embed

        # ========== BUTTON VIEW ==========
        class StatsView(View):
            def __init__(self):
                super().__init__(timeout=120)
                self.index = 0  # current page

            async def update(self, interaction):
                await interaction.response.edit_message(
                    embed=make_embed(self.index),
                    view=self
                )

            @discord.ui.button(label="⬅️ Prev", style=discord.ButtonStyle.secondary)
            async def prev_btn(self, interaction: discord.Interaction, button: Button):
                if interaction.user.id != ctx.author.id:
                    return await interaction.response.send_message(
                        "Not your stats.", ephemeral=True
                    )
                self.index = (self.index - 1) % total_pages
                await self.update(interaction)

            @discord.ui.button(label="Next ➡️", style=discord.ButtonStyle.primary)
            async def next_btn(self, interaction: discord.Interaction, button: Button):
                if interaction.user.id != ctx.author.id:
                    return await interaction.response.send_message(
                        "Not your stats.", ephemeral=True
                    )
                self.index = (self.index + 1) % total_pages
                await self.update(interaction)

        view = StatsView()
        await ctx.send(embed=make_embed(0), view=view)


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
            "`!cocktimes` — Show all cock fight times\n"
        )
        await ctx.send(msg)

