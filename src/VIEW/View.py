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
    def get_input(self) -> str:
        pass