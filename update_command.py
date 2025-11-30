# update_command.py
from discord.ext import commands
from config import UPDATE_MESSAGE_30   # ← ייבוא של העדכון מהקונפיג

def setup_update_command(bot: commands.Bot):

    @bot.command(name="update")
    async def update_cmd(ctx):
        await ctx.send(embed=UPDATE_MESSAGE_30)
