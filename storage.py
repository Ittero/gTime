import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

GAMES_FILE = DATA_DIR / "games.json"
STATS_FILE = DATA_DIR / "stats.json"


def load_games() -> dict:
    if not GAMES_FILE.exists():
        raise FileNotFoundError("games.json not found")
    with open(GAMES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_stats(games: dict) -> None:
    # Якщо stats.json не існує або порожній — створюємо
    if not STATS_FILE.exists() or STATS_FILE.stat().st_size == 0:
        stats = {"games": {}}
    else:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            stats = json.load(f)

    # Додаємо нові ігри, не чіпаючи старі
    for game_name in games.keys():
        if game_name not in stats["games"]:
            stats["games"][game_name] = {
                "total_time": 0,
                "sessions": []
            }

    save_stats(stats)



def load_stats(games: dict) -> dict:
    ensure_stats(games)
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)



def save_stats(stats: dict) -> None:
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)


def add_session(game_name: str, start_ts: float, end_ts: float, games: dict) -> None:
    stats = load_stats(games)

    duration = int(end_ts - start_ts)
    session = {
        "start": datetime.fromtimestamp(start_ts).strftime("%Y-%m-%d %H:%M:%S"),
        "end": datetime.fromtimestamp(end_ts).strftime("%Y-%m-%d %H:%M:%S"),
        "duration": duration
    }

    stats["games"][game_name]["sessions"].append(session)
    stats["games"][game_name]["total_time"] += duration

    save_stats(stats)
