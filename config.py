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
# ========= RARITY PRIORITY ========= #
# Higher number = rarer achievement
RARITY_PRIORITY = {
    "common": 1,
    "uncommon": 2,
    "rare": 3,
    "epic": 4,
    "legendary": 5,
    "mythic": 6,
    "god": 7
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
    #rewards 
    "friend_of_pork": {
        "name": "Friend of Pork",
        "description": "You answered John Pork’s call. He saved your number. Forever.",
        "rarity": "uncommon",
        "chance": 0.0   # awarded manually by event logic
    },
    "chest_luck_blessed": {
        "name": "Blessed by the Chest",
        "description": "You opened the Mysterious Chest and the loot loved you back.",
        "rarity": "uncommon",
        "chance": 0.0
    },

    "chest_luck_cursed": {
        "name": "Cursed by the Chest",
        "description": "The chest punished your curiosity. Painfully.",
        "rarity": "uncommon",
        "chance": 0.0
    },

    "reckless_chest_kicker": {
        "name": "Reckless Chest Kicker",
        "description": "You kicked a magical chest for absolutely no reason.",
        "rarity": "common",
        "chance": 0.0
    },

    "cowardly_escape_artist": {
        "name": "Cowardly Escape Artist",
        "description": "You ran away from the mysterious chest. Pathetic. But understandable.",
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
    "abducted_mid_edge": {
        "name": "Abducted Mid-Edge",
        "description": "Aliens abducted you mid-stroke. They returned you slightly different.",
        "rarity": "epic",
        "chance": 0.0   # triggered manually like Blue Balls
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
    "almost_there": {
        "name": "Almost There",
        "description": "You got dangerously close… but held back like a champion.",
        "rarity": "uncommon",
        "chance": 0.07
    },

    "sticky_situation": {
        "name": "Sticky Situation",
        "description": "Your hands encountered… unexpected resistance.",
        "rarity": "common",
        "chance": 0.1
    },

    "goon_whisper": {
        "name": "Goon Whisper",
        "description": "A faint voice from another realm encouraged you forward.",
        "rarity": "uncommon",
        "chance": 0.07
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
    "pink_panther_balls": {
        "name": "Pink Panther Balls",
        "description": "You reached a cartoonishly dangerous level of edging pressure.",
        "rarity": "rare",
        "chance": 0.06
    },
    "jewballs": {
        "name": "Mystic Jewballs",
        "description": "You saw old Rabbi in your dream whispering you: Don not spill your seed in vain",
        "rarity": "epic",
        "chance": 0.01
    },

    "milk_overflow": {
        "name": "Milk Overflow",
        "description": "Your essence surged beyond containment and overflowed.",
        "rarity": "epic",
        "chance": 0.015
    },
    "butterfingers": {
        "name": "Butterfingers",
        "description": "You fumbled at the worst possible moment. Truly tragic.",
        "rarity": "common",
        "chance": 0.15
    }, 
    "you_good_bro": {
        "name": "You Good Bro?",
        "description": "Even the bot had to stop and check on you.",
        "rarity": "uncommon",
        "chance": 0.10
    },
    "edge_goblin": {
        "name": "Edge Goblin",
        "description": "You lurk in the shadows and edge at inconvenient hours.",
        "rarity": "rare",
        "chance": 0.05
    }, 
    "professional_overthinker": {
        "name": "Professional Overthinker",
        "description": "You stared at it for way too long trying to make a decision.",
        "rarity": "uncommon",
        "chance": 0.13
    }, 
    "oops_my_bad": {
        "name": "Oops, My Bad…",
        "description": "You clicked when you shouldn't have. A classic goon misfire.",
        "rarity": "uncommon",
        "chance": 0.12
    }, 
    "area_69_survivor": {
        "name": "Area 69 Survivor",
        "description": "You saw things no ordinary man should ever edge.",
        "rarity": "rare",
        "chance": 0.04
    }, 
    "elven_edgecraft": {
        "name": "Elven Edgecraft",
        "description": "You mastered a delicate technique whispered among ancient elves.",
        "rarity": "uncommon",
        "chance": 0.14
    }, 
    "one_handed_hero": {
        "name": "Prophecy of the One-Handed Hero",
        "description": "Ancient scrolls foretold your powerful yet confusing technique.",
        "rarity": "uncommon",
        "chance": 0.13
    }, 
    "wishmasters_curse": {
        "name": "Wishmaster’s Curse",
        "description": "You wished for more stamina. The genie misheard you.",
        "rarity": "rare",
        "chance": 0.04
    }, 
    "dragon_breath": {
        "name": "Dragon’s Breath Reaction",
        "description": "A dragon saw your movements and exhaled in disappointment… or admiration.",
        "rarity": "uncommon",
        "chance": 0.16
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

    "omega_goon": {
        "name": "Omega Goon",
        "description": "You channeled every ounce of cosmic goon energy inside you.",
        "rarity": "mythic",
        "chance": 0.002
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


UPDATE_MESSAGE_30 = discord.Embed(
    title="🌌 עדכון 3.0 — עידן ההרפתקאות",
    description=(
        "📜 **כך נאמר במגילת מסטאר גונוואיי:**\n"
        "*\"מי שמוכן לפגוש את הבלתי־צפוי — מגלה שהיקום עצמו רוצה לשחק איתו.\"*\n\n"
        "מאז פרק 2.5, העולם החל לרעוד: קולות מעבר לזמן, תיבות שמופיעות משום מקום, "
        "וחזירים שמצלצלים באמצע הלילה. פרק 3.0 אינו רק עדכון — הוא פתיחת הדלת "
        "ליקום חי, אינטראקטיבי ותזזיתי.\n\n"
        "✨ **זהו עידן ההרפתקאות.**"
    ),
    color=discord.Color.purple()
)

UPDATE_MESSAGE_30.add_field(
    name="👽 Alien Abduction — חטיפת חייזרים",
    value=(
        "• 0.7% סיכוי להיחטף באמצע הגון\n"
        "• 7 דקות של בלבול קוסמי\n"
        "• 50% לקבלת 'טכניקת על' (בוסט XP)\n"
        "• הישג חדש: **Abducted Mid-Edge**\n\n"
        "_“גם מי שמופרע באחת… חוזר עם תובנה שלא ביקש.”_"
    ),
    inline=False
)

UPDATE_MESSAGE_30.add_field(
    name="📞🐷 John Pork Calls — שיחת פורק",
    value=(
        "• מופיע אקראית כל 3 שעות\n"
        "• הראשון שעונה זוכה ב־70 XP\n"
        "• כפתור אינטראקטיבי חדש\n"
        "• הישג חדש: **Friend of Pork**\n\n"
        "_“מי שעונה לפורק — לעולם אינו לבד.”_"
    ),
    inline=False
)

UPDATE_MESSAGE_30.add_field(
    name="💼 Mysterious Chest — התיבה המסתורית",
    value=(
        "• בחר: פתח בעדינות / בעיטה / בריחה\n"
        "• תוצאות רנדומליות טובות ורעות\n"
        "• 4 הישגים חדשים:\n"
        "   🟣 Blessed by the Chest\n"
        "   🔴 Cursed by the Chest\n"
        "   🟡 Reckless Chest Kicker\n"
        "   ⚪ Cowardly Escape Artist\n\n"
        "_“הבחירה שלך — הגורל שלך.”_"
    ),
    inline=False
)

UPDATE_MESSAGE_30.add_field(
    name="⚔️ מפגשים אקראיים בעולם",
    value=(
        "העולם של גונוואיי חי: קרבות, תיבות, פורק וחייזרים מתרחשים "
        "בזמנים אקראיים — וכל גונר חווה מסע שונה."
    ),
    inline=False
)
UPDATE_MESSAGE_30.add_field(
    name="🐓⚔️ Beat The Cock — שיפורים ותיקונים",
    value=(
        "• תוקן הבאג שגרם לקרבות להופיע רק פעם אחת ביום או לא לצאת בכלל\n"
        "• כעת נוצרות **4 שעות רנדומליות בכל יום**, מחוץ לשעות 02:00–08:00\n"
        "• הקרבות יציבים יותר, הסנכרון שופר, והאנימציה רצה חלק\n"
        "• פקודה חדשה: **!cocktimes** — מציגה את זמני הקרבות של היום\n\n"
        "_“הקרב תמיד מגיע… רק צריך לדעת מתי.”_"
    ),
    inline=False
)


UPDATE_MESSAGE_30.set_footer(text="Master Goonway • גרסה 3.0 • הדרך נפתחת מחדש")
