from discord.ext import commands
import discord

def setup_update_command(bot: commands.Bot):

    @bot.command(name="update")
    async def update_cmd(ctx):

        embed = discord.Embed(
            title="🔥 עדכון 2.5 — מתקפת הגונוואיי",
            description=(
                "📜 **כך הכריז מסטאר גונוואיי על העדכון החדש:**\n"
                "*\"הקרב אינו בין שני לוחמים —\n"
                "אלא בין האדם לבין היכולת שלו להתייצב מול הרגע.\n"
                "כל גון הוא נשימה של אמת,\n"
                "וכל ניצחון הוא חיזוק לרוח.\"*\n\n"

                "⚔️ **Beat The Cock Fight – הקרב החדש**\n"
                "• שני לוחמים בלבד\n"
                "• שלב **READY** חובה\n"
                "• קרב אנימציה חי של **10 שניות**\n"
                "• המנצח: **+50 XP**\n"
                "• הישג חדש: **הגונר המהיר במערב**\n\n"

                "⏰ **4 הופעות ביום**, בזמנים אקראיים.\n"
            ),
            color=discord.Color.gold()
        )

        await ctx.send(embed=embed)