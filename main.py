from storage import load_games, ensure_stats
from tracker import GameTracker
from logger import logger

def main():
    logger.info("gTime started")
    games = load_games()
    logger.info(f"Loaded games: {', '.join(games.keys())}")

    ensure_stats(games)

    tracker = GameTracker(games)

    try:
        tracker.run(interval=3)
    except KeyboardInterrupt:
        logger.info("gTime stopped by user (Ctrl+C)")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
