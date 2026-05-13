"""Modulo per la gestione dell'interfaccia utente (View)."""

from abc import ABC, abstractmethod


class BaseView(ABC):
    """Classe astratta base per la gestione della vista."""

    @abstractmethod
    def render(self, game_state: dict) -> None:
        pass

    @abstractmethod
    def show_error(self, message: str) -> None:
        pass

    @abstractmethod
    def show_victory(self, player_id: int) -> None:
        pass

    @abstractmethod
    def show_exit(self, winner_id: int) -> None:
        pass

    @abstractmethod
    def get_input(self) -> str:
        pass

    @abstractmethod
    def show_initial_message(self) -> None:
        pass

    @abstractmethod
    def show_help(self) -> None:
        pass

    @abstractmethod
    def show_exit_message(self) -> None:
        pass

    @abstractmethod
    def prompt_new_game(self) -> str:
        pass
