"""Modulo per la gestione dell'interfaccia utente (View)."""

from abc import ABC, abstractmethod


class BaseView(ABC):
    """Classe astratta base per la gestione della vista."""

    @abstractmethod
    def render(self, game_state: dict) -> None:
        """Disegna lo stato completo del gioco."""

    @abstractmethod
    def show_error(self, message: str) -> None:
        """Mostra un messaggio di errore."""

    @abstractmethod
    def show_victory(self, player_id: int) -> None:
        """Mostra il messaggio di vittoria."""

    @abstractmethod
    def get_input(self) -> str:
        """Richiede e restituisce l'input dell'utente."""

    @abstractmethod
    def show_exit(self, winner_id: int) -> None:
        """Mostra il messaggio di uscita con il vincitore."""

    @abstractmethod
    def show_exit_message(self) -> None:
        """Mostra il messaggio di chiusura dell'applicazione."""

    @abstractmethod
    def show_initial_message(self) -> None:
        """Mostra il messaggio di benvenuto."""

    @abstractmethod
    def show_help(self) -> None:
        """Mostra le regole e i comandi del gioco."""

    @abstractmethod
    def show_timeout(self, player_id: int) -> None:
        """Mostra il messaggio di tempo scaduto per il giocatore."""

    @abstractmethod
    def prompt_new_game(self) -> str:
        """Chiede se si vuole iniziare una nuova partita. Restituisce 's' o 'n'."""

    @abstractmethod
    def prompt_replay(self) -> str:
        """Chiede se si vuole vedere il replay della partita. Restituisce 's' o 'n'."""

    @abstractmethod
    def prompt_game_settings(self) -> tuple[bool, float]:
        """Mostra il menu di configurazione. Restituisce (usa_tempo, secondi_totali)."""

    def show_player_resigned(self, player_id: int) -> None:  # noqa: B027
        """Mostra il messaggio di abbandono in modalità 4P (partita continua).

        Implementazione di default non-astratta: le view possono sovrascriverla
        o usare questa versione base che non fa nulla.
        """

    @abstractmethod
    def show_move_history(self, move_history: list[dict], num_players: int) -> None:
        """Mostra la cronologia delle mosse effettuate nella partita.

        Args:
            move_history (list[dict]): Lista di mosse con player_id, move_type, notation
            num_players (int): Numero di giocatori (2 o 4)

        """
