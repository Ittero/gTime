from storage import load_games, ensure_stats
from tracker import GameTracker

def main():
    games = load_games()
    ensure_stats(games)

    tracker = GameTracker(games)

    print("gTime запущено. Натисніть Ctrl+C, щоб зупинити.")
    tracker.run(interval=3)

if __name__ == "__main__":
    main()
