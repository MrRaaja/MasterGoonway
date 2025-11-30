# bot.py
from dotenv import load_dotenv
load_dotenv()

import discord
from discord.ext import commands

from config import TOKEN, CHANNEL_ID, UPDATE_MESSAGE_30
from data_manager import load_data, ensure_jar, save_data

from goon_commands import setup_goon_commands
from other_commands import setup_other_commands
from scheduler import setup_daily_scheduler
from update_command import setup_update_command

from cock_fight import setup_cock_fight   # we initialize the system here
from john_pork import setup_john_pork
from mysterious_chest import setup_mysterious_chest


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
setup_john_pork(bot, data)
setup_mysterious_chest(bot, data)

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
            await channel.send(embed=UPDATE_MESSAGE_30)
            print("Sent Update 3.0 announcement.")
    except Exception as e:
        print("Failed to send update message:", e)

    # Start daily quote scheduler
    setup_daily_scheduler(bot)

    from cock_fight import setup_cock_fight as cf

    try:
        cf.generate_daily_cock_times.start()
        cf.monitor_cock_times.start()
        print("Cockfight schedulers started.")
    except RuntimeError:
        pass

    try:    
        from john_pork import setup_john_pork as jp
        jp.scheduler.start()
        print("John Pork scheduler started.")
    except RuntimeError:
        # Happens on reload — safe to ignore
        pass
    except Exception as e:
        print("Failed to start John Pork", e)
    # Start Mysterious Chest scheduler
    try:
        from mysterious_chest import setup_mysterious_chest as mc
        mc.scheduler.start()
        print("Mysterious Chest scheduler started.")
    except RuntimeError:
        pass
    except Exception as e:
        print("Failed to start Mysterious Chest scheduler:", e)


@bot.event
async def on_disconnect():
    # Just to be safe
    save_data(data)
    print("Bot disconnected — data saved.")


# ============================
# Run Bot
# ============================

bot.run(TOKEN)
