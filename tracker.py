import time
from datetime import datetime
import psutil
from storage import add_session
from logger import set_current_game, clear_current_game


class GameTracker:
    def __init__(self, games: dict):
        self.games = games  # { game_name: process_name }
        self.active_sessions = {}

    def _get_running_processes(self) -> set:
        return {p.info["name"] for p in psutil.process_iter(attrs=["name"])}

    def _start_session(self, game_name: str):
        self.active_sessions[game_name] = time.time()
        set_current_game(game_name)

    def _end_session(self, game_name: str):
        start_ts = self.active_sessions.pop(game_name)
        end_ts = time.time()
        clear_current_game()  
        add_session(game_name, start_ts, end_ts, self.games)

    def tick(self):
        running_processes = self._get_running_processes()
        for game_name, process_name in self.games.items():
            is_running = process_name in running_processes
            is_active = game_name in self.active_sessions

            if is_running and not is_active:
                self._start_session(game_name)
            elif not is_running and is_active:
                self._end_session(game_name)

    def run(self, interval: int = 3):
        try:
            while True:
                self.tick()
                time.sleep(interval)
        except KeyboardInterrupt:
            # Закриваємо всі активні сесії перед виходом
            for game_name in list(self.active_sessions.keys()):
                self._end_session(game_name)
            print("\ngTime зупинено. Дані збережено. До зустрічі!")
