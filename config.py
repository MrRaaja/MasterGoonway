# config.py
import discord
import os

TOKEN = os.getenv("GOONBOT_TOKEN")
CHANNEL_ID = int(os.getenv("GOONBOT_CHANNEL_ID", "0"))
# ========= BASIC CONFIG ========= #

DATA_FILE = "goon_data.json"
QUOTES_FILE = "quotes.txt"

ESSENCE_NAME = "Goon Essence Jar"
BASE_ESSENCE_PER_GOON = 3      # "ml" before bonus
BASE_XP_PER_GOON = 10          # XP before bonus

# Jar milestones in ml
JAR_MILESTONES_ML = [
    1000,    # 1 L
    3000,    # 3 L
    5000,    # 5 L
    10000,   # 10 L
    20000,   # 20 L
    50000,   # 50 L
    100000   # 100 L
]

# ========= LEVELS ========= #

LEVELS = [
    ("Newbie-Edger", 0),
    ("Mild Gooner", 50),
    ("Steady Edgelord", 150),
    ("Intermediate-Gooner", 300),
    ("Deep Wanderer", 500),
    ("Master Gooner", 700),
    ("Lord Goon", 1000),
    ("Goon Ascended", 1500),
    ("The Eternal Goon", 2500),
    ("Astral Gooner", 4000),
    ("Void Walker", 6000),
    ("Edge Prophet", 9000),
    ("Goon Whisperer", 12000),
    ("Temporal Drifter", 16000),
    ("Celestial Edgelord", 20000),
    ("Spiritbound Goon", 26000),
    ("Dimension Warden", 33000),
    ("Infinite Gooner", 42000),
    ("Omni-Edger", 55000),
    ("Transcendent Wanderer", 70000),
    ("Primordial Goon", 85000),
    ("Cosmic Master Gooner", 100000),
    ("The One Who Edges Time", 150000),
    ("Beyond All Goon", 200000),

    # Ultra endgame
    ("The Endless Edge", 1_000_000),
    ("Keeper of Infinite Goon", 2_500_000),
    ("Oracle of Stillness", 5_000_000),
    ("The Final Wanderer", 10_000_000),
    ("Edgewright of Eternity", 25_000_000),
    ("The Silent Cosmos", 50_000_000),
    ("Beyond Concept of Goon", 75_000_000),
    ("One-Above-All Gooners", 100_000_000)
]

# ========= RARITY ICONS ========= #

RARITY_COLORS = {
    "common": "⚪",
    "uncommon": "🟢",
    "rare": "🔵",
    "epic": "🟣",
    "legendary": "🟡",
    "mythic": "🔴",
    "god": "✨"
}

# ========= ACHIEVEMENTS ========= #
# chance = 0 means "not random" (awarded by logic)

ACHIEVEMENTS = {
    "first_goon": {
        "name": "First Goon",
        "description": "Used !goon for the first time.",
        "rarity": "common",
        "chance": 0.0
    },

    # Sickness
    "blue_balls": {
        "name": "Blue Balls",
        "description": "You were struck by the sickness and forced to rest.",
        "rarity": "rare",
        "chance": 0.0
    },

    # Random loot-style
    "blood_cum": {
        "name": "Blood Cum",
        "description": "A rare surge of crimson edge energy flows through you.",
        "rarity": "rare",
        "chance": 0.03
    },
    "wet_dream": {
        "name": "Wet Dream",
        "description": "A surreal dream vision visited you.",
        "rarity": "common",
        "chance": 0.10
    },
    "cum_pee": {
        "name": "Cum Pee",
        "description": "A mysterious fluid phenomenon blessed your aura.",
        "rarity": "epic",
        "chance": 0.01
    },
    "frozen_edge": {
        "name": "Frozen Edge",
        "description": "You reached absolute stillness of mind.",
        "rarity": "rare",
        "chance": 0.05
    },
    "shadow_goon": {
        "name": "Shadow Goon",
        "description": "You glimpsed the goon dimension beyond the veil.",
        "rarity": "epic",
        "chance": 0.02
    },

    # Legendary / mythic / god-tier
    "cosmic_leakage": {
        "name": "Cosmic Leakage",
        "description": "You overflowed with energy from beyond the stars.",
        "rarity": "legendary",
        "chance": 0.005
    },
    "astral_overflow": {
        "name": "Astral Overflow",
        "description": "Your soul briefly disconnected from time.",
        "rarity": "mythic",
        "chance": 0.002
    },
    "quantum_burst": {
        "name": "Quantum Burst",
        "description": "You generated a fluctuation in spacetime.",
        "rarity": "legendary",
        "chance": 0.001
    },
    "Vagina_from_China": {
        "name": "Vagina from China",
        "description": "You have found the holy Vagina from China -Ching Chang Bing Bong.",
        "rarity": "legendary",
        "chance": 0.001
    },
    "temporal_rift": {
        "name": "Temporal Rift",
        "description": "You cracked the edge of reality momentarily.",
        "rarity": "mythic",
        "chance": 0.0005
    },
    "final_drip": {
        "name": "The Final Drip",
        "description": "A myth whispered by ancient gooners… you touched infinity.",
        "rarity": "god",
        "chance": 0.0001
    },
        "fastest_gooner_west": {
        "name": "Fastest Gooner of the West",
        "rarity": "epic",
        "description": "Won a Beat The Cock duel by jerking off fast enough."
    }
}
UPDATE_MESSAGE_20 = (
    "🌒✨ *מגילת מסטאר גונוואיי – עדכון 2.0* ✨🌘\n\n"
    "מסופר שכאשר הזמן עוד לא נאחז בשמות, וכאשר השקט היה רם יותר מן הרעש, "
    "צעד מסטאר גונוואיי בין עולמות שאיש לא העז לגעת בהם. הוא לא חיפש כוח, "
    "לא תהילה, ולא הכרה – אלא הבין שחכמה אמיתית נוצרת דווקא מתוך המתנה, "
    "נשימה, ועומק פנימי שלא מתפשר על מהירות.\n\n"
    "לאורך דרכו גילה המסטאר שהמסע האמיתי אינו קדימה – אלא פנימה. "
    "כי רק מי שמסוגל לעצור, להתבונן, ולהקשיב לרגע אחד עד סופו, "
    "מגלה בתוכו שערים שאחרים לעולם לא יראו.\n\n"
    "ועכשיו, לאחר נדודים בין סדקי הזמן, שב מסטאר גונוואיי אל תלמידיו עם תובנות חדשות, "
    "חזקות ועמוקות מאי פעם. זהו פרק חדש במסע – מסע של עומק, איזון והבנה.\n\n"
    "🔮 *אלו הם אוצרותיו החדשים:* \n\n"
    "🌡️ **מחלת ‘כדורים כחולים’** – שיעור קדום בסבלנות: לעיתים הגוף דורש מנוחה "
    "כדי שהרוח תוכל להמשיך לנוע. שעה אחת של הפוגה מעצימה את הדרך.\n\n"
    "💧 **צנצנת מהות הגון – Goon Essence Jar**\n"
    "כל רגע של התמסרות מוסיף טיפה חדשה לצנצנת הגדולה. וכאשר היא חוצה מדרגות של ליטרים, "
    "העולם כולו מרגיש את התנודה.\n\n"
    "⏳ **כוח ההמתנה**\n"
    "מסטאר גונוואיי גילה שהמתנה מעבר לנדרש מעניקה תובנה עמוקה יותר. "
    "הסבלן זוכה פי כמה: יותר XP, יותר מהות, יותר התקדמות.\n\n"
    "🎲 **הישגים נדירים**\n"
    "על השביל, לעיתים מבלי לשים לב, מופיעים סימנים מהיקום: ‘חלום רטוב’, ‘שבר-זמן’, "
    "‘דממת הצל’, ‘דליפת־כוכבים’, ועוד מתנות שהיקום מעניק רק למוכנים באמת.\n\n"
    "🏆 **מדרגות חוכמה חדשות**\n"
    "שערים נפתחו לרמות עמוקות יותר בתודעה: מן ‘גונר בינוני’ ועד ‘זה שמעל לכל גונר’. "
    "המסע כעת רחב יותר, עמוק יותר, ומשמעותי יותר.\n\n"
    "🕛 **מחשבת חצות**\n"
    "בכל לילה, בדיוק ב־00:00, שולח המסטאר פסוק של שקט – מחשבה אחת שמנקה את הרעש, "
    "מאזנת את הלב ומכוונת את הדרך.\n\n"
    "ולבסוף אמר מסטאר גונוואיי:\n"
    "“הדרך אינה נמדדת במרחק, אלא בכמה רגעים הצלחת באמת להיות נוכח.”\n\n"
    "———\n\n"
    "🔍 *סיכום קצר וברור של עדכון 2.0:*\n"
    "• מערכת מחלה – ‘כדורים כחולים’ (Rest 1h)\n"
    "• מערכת צנצנת מהות הגון (Essence Jar + milestones)\n"
    "• בונוס XP ומהות לפי זמן המתנה\n"
    "• הישגים רנדומליים נדירים לפי אחוזי נדירות\n"
    "• מערכת רמות חדשה ומורחבת\n"
    "• פקודות חדשות: !jar, !update\n\n"
    "ברוכים הבאים לעדכון 2.0 – דרכו המתחדשת של מסטאר גונוואיי."
)
UPDATE_MESSAGE_25 = discord.Embed(
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


