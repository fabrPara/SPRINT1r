"""Tests for quitting the game via the abbandona command."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.CONTROLLER.GameController import GameController
from src.MODEL.QuoridorGame import QuoridorGame


class DummyView:
    """Dinamica di test per la vista CLI fittizia del gioco."""

    def __init__(self):
        self.inputs = ["abbandona"]
        self.exited = False

    def render(self, game_state: dict) -> None:
        pass

    def show_error(self, message: str) -> None:
        pass

    def show_victory(self, player_id: int) -> None:
        pass

    def show_exit(self, winner_id: int) -> None:
        self.exited = True
        self.winner_id = winner_id

    def show_exit_message(self) -> None:
        pass

    def show_player_resigned(self, player_id: int) -> None:
        pass

    def prompt_new_game(self) -> str:
        return "n"

    def prompt_game_settings(self) -> tuple[bool, float]:
        return (False, 180.0)

    def prompt_num_players(self) -> int:
        return 2

    def show_initial_message(self) -> None:
        pass

    def get_input(self) -> str:
        return self.inputs.pop(0) if self.inputs else ""


def test_abbandona_stops_game():
    """Verifica che il comando abbandona interrompa la partita."""
    model = QuoridorGame()
    view = DummyView()
    controller = GameController(model, view)

    controller.start_game()

    assert controller._exit_requested is True
    assert view.exited is True
    assert view.winner_id == 2
    assert model.get_game_state()["winner"] == 2
