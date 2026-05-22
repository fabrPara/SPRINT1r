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
    def show_draw(self) -> None:
        pass

    @abstractmethod
    def show_draw_declined(self) -> None:
        pass

    @abstractmethod
    def prompt_draw_answer(self, opponent_id: int) -> str:
        pass

    @abstractmethod
    def get_input(self) -> str:
        pass
