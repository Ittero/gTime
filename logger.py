import logging
import atexit

logging.basicConfig(
    filename="logs/gtime.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger("gTime")

current_game = None


def set_current_game(game_name: str):
    global current_game
    current_game = game_name
    logger.info(f"Game started: {game_name}")


def clear_current_game():
    global current_game
    if current_game:
        logger.info(f"Game stopped: {current_game}")
        current_game = None


def on_exit():
    if current_game:
        logger.info(f"gTime stopped while game was running: {current_game}")
    else:
        logger.info("gTime stopped (no active game)")


atexit.register(on_exit)
