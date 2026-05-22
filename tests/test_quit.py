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

    def show_initial_message(self) -> None:
        pass

    def show_help(self) -> None:
        pass

    def prompt_new_game(self) -> str:
        return "n"

    def show_draw(self) -> None:
        self.draw = True

    def show_draw_declined(self) -> None:
        self.draw_declined = True

    def prompt_draw_answer(self, opponent_id: int) -> str:
        return self.inputs.pop(0) if self.inputs else "n"

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


def test_pattta_accepted_ends_game():
    """Verifica che l'offerta di patta accettata termini la partita."""
    model = QuoridorGame()
    view = DummyView()
    view.inputs = ["patta", "s"]
    controller = GameController(model, view)

    controller.start_game()

    assert model.is_draw() is True
    assert hasattr(view, "draw") and view.draw is True


def test_pattta_declined_continues_game():
    """Verifica che l'offerta di patta rifiutata continui la partita."""
    model = QuoridorGame()
    view = DummyView()
    # Offer draw and decline, then immediately exit by supplying 'exit'
    view.inputs = ["patta", "n", "exit"]
    controller = GameController(model, view)

    controller.start_game()

    assert model.is_draw() is False
    assert hasattr(view, "draw_declined") and view.draw_declined is True
