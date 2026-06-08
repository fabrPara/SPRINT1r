from src.CONTROLLER.GameController import GameController
from src.MODEL.QuoridorGame import QuoridorGame
from src.VIEW.BaseView import BaseView


class MockView(BaseView):
    """Mock minimale per soddisfare l'interfaccia di BaseView."""

    def render(self, game_state: dict) -> None:
        pass

    def show_error(self, message: str) -> None:
        pass

    def show_victory(self, player_id: int) -> None:
        pass

    def get_input(self) -> str:
        return "e3"

    def show_exit(self, winner_id: int) -> None:
        pass

    def show_exit_message(self) -> None:
        pass

    def show_initial_message(self) -> None:
        pass

    def show_help(self) -> None:
        pass

    def show_timeout(self, player_id: int) -> None:
        pass

    def prompt_new_game(self) -> str:
        return "n"

    def prompt_replay(self) -> str:
        return "n"

    def prompt_game_settings(self) -> tuple[bool, float]:
        return (False, 180.0)

    def show_move_history(
        self, move_history: list[dict], num_players: int
    ) -> None:
        pass


def test_controller_initialization():
    """CE Valida: Verifica la mappatura corretta delle colonne (A-I)."""
    model = QuoridorGame(num_players=2)
    view = MockView()
    controller = GameController(model, view)

    assert controller._COL_MAP["A"] == 0
    assert controller._COL_MAP["I"] == 8
    assert controller._is_timed_game is False


def test_clocks_setup_boundaries():
    """VL: Inizializzazione corretta dei timer predefiniti (180 secondi)."""
    model = QuoridorGame(num_players=2)
    view = MockView()
    controller = GameController(model, view)

    assert controller._players_clocks[1] == 180.0
    assert controller._players_clocks[2] == 180.0