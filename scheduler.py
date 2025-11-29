# scheduler.py

import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from config import CHANNEL_ID
from data_manager import load_quotes

_scheduler = None

def setup_daily_scheduler(bot):
    global _scheduler
    if _scheduler is not None and _scheduler.running:
        return

    _scheduler = AsyncIOScheduler()

    async def send_daily_quote():
        channel = bot.get_channel(CHANNEL_ID)
        if not channel:
            return
        quotes = load_quotes()
        if not quotes:
            return
        quote = random.choice(quotes)
        await channel.send(f"🌙 **Daily Goon Wisdom (00:00):**\n{quote}")

    # Every day at 00:00 (server local time)
    _scheduler.add_job(send_daily_quote, CronTrigger(hour=0, minute=0))
    _scheduler.start()
