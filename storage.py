import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

GAMES_FILE = DATA_DIR / "games.json"
STATS_FILE = DATA_DIR / "stats.json"

# Завантаження ігор з games.json
def load_games() -> dict:
    if not GAMES_FILE.exists():
        raise FileNotFoundError("games.json not found")

    with open(GAMES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
    # Ініціалізація stats.json
def init_stats(games: dict) -> None:
    if STATS_FILE.exists():
        return

    stats = {"games": {}}

    for game_name in games.keys():
        stats["games"][game_name] = {
            "total_time": 0,
            "sessions": []
        }

    DATA_DIR.mkdir(exist_ok=True)

    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

# Завантаження статистики з stats.json
def load_stats() -> dict:
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Збереження статистики в stats.json
def save_stats(stats: dict) -> None:
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

# Додавання ігрової сесії
def add_session(game_name: str, start_ts: float, end_ts: float) -> None:
    stats = load_stats()

    duration = int(end_ts - start_ts)

    session = {
        "start": datetime.fromtimestamp(start_ts).strftime("%Y-%m-%d %H:%M:%S"),
        "end": datetime.fromtimestamp(end_ts).strftime("%Y-%m-%d %H:%M:%S"),
        "duration": duration
    }

    stats["games"][game_name]["sessions"].append(session)
    stats["games"][game_name]["total_time"] += duration

    save_stats(stats)
