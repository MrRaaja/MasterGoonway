# cooldowns.py

from config import LEVELS

def get_level(xp: int) -> str:
    current = LEVELS[0][0]
    for name, req in LEVELS:
        if xp >= req:
            current = name
    return current

def get_cooldown_seconds(xp: int) -> int:
    """Tiered cooldown:
       0-99 XP   ->  900s (15m)
       100-299   ->  600s (10m)
       300-599   ->  300s (5m)
       600-999   ->  120s (2m)
       1000+     ->   30s
    """
    if xp >= 1000:
        return 30
    elif xp >= 600:
        return 120
    elif xp >= 300:
        return 300
    elif xp >= 100:
        return 600
    else:
        return 900
