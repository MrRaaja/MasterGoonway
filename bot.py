# bot.py
from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands

from config import TOKEN, CHANNEL_ID, UPDATE_MESSAGE_25
from data_manager import load_data, ensure_jar, save_data

from goon_commands import setup_goon_commands
from other_commands import setup_other_commands
from scheduler import setup_daily_scheduler
from update_command import setup_update_command

from cock_fight import setup_cock_fight   # we initialize the system here


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Load persistent data
data = load_data()
ensure_jar(data)


# ============================
# Register Commands & Systems
# ============================

setup_goon_commands(bot, data)
setup_other_commands(bot, data)
setup_update_command(bot)

# Setup cockfight; this defines auto_cockfight inside it
setup_cock_fight(bot, data)


# ============================
# Events
# ============================

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # Send update message (only once per boot)
    try:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(embed=UPDATE_MESSAGE_25)
            print("Sent Update 2.5 announcement.")
    except Exception as e:
        print("Failed to send update message:", e)

    # Start daily quote scheduler
    setup_daily_scheduler(bot)

    # Start automatic cockfight scheduler
    try:
        # Imported through setup function: setup_cock_fight.auto_cockfight
        from cock_fight import setup_cock_fight as cf
        cf.auto_cockfight.start()
        print("Auto cockfight scheduler started.")
    except RuntimeError:
        # Happens on reload — safe to ignore
        pass
    except Exception as e:
        print("Failed to start auto_cockfight:", e)


@bot.event
async def on_disconnect():
    # Just to be safe
    save_data(data)
    print("Bot disconnected — data saved.")


# ============================
# Run Bot
# ============================

bot.run(TOKEN)
