# data_manager.py

import json
import os
from config import DATA_FILE, QUOTES_FILE

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def ensure_user(data, user_id: str):
    """Initialize missing keys for new OR old users."""
    if user_id not in data:
        # Fresh user
        data[user_id] = {
            "xp": 0,
            "achievements": [],
            "last_goon_time": 0,
            "sick_until": 0,
            "essence_given": 0
        }
        return

    # Patch OLD users who are missing fields
    user = data[user_id]

    if "xp" not in user:
        user["xp"] = 0
    if "achievements" not in user:
        user["achievements"] = []
    if "last_goon_time" not in user:
        user["last_goon_time"] = 0
    if "sick_until" not in user:
        user["sick_until"] = 0
    if "essence_given" not in user:
        user["essence_given"] = 0

def ensure_jar(data):
    if "_jar" not in data:
        data["_jar"] = {
            "total_ml": 0,
            "last_milestone": 0
        }

def load_quotes():
    if not os.path.exists(QUOTES_FILE):
        return []
    with open(QUOTES_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]
