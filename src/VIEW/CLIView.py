"""Modulo per l'interfaccia a riga di comando (CLI) del gioco."""

from rich.console import Console
from rich.table import Table

from .BaseView import BaseView


class CLIView(BaseView):
    """Implementazione della View tramite Command Line Interface (CLI).

    Utilizza la libreria Rich per formattare l'output nel terminale.
    """

    def __init__(self):
        """Inizializza la CLI View creando un'istanza della Console di Rich."""
        self._console = Console()

    def render(self, game_state: dict) -> None:
        """Disegna lo stato completo del gioco aggiornato.

        Args:
            game_state (dict): Dizionario con lo stato del gioco.
                               Ci si aspetta contenga 'board' e 'players'.

        """
        self._console.clear()

        players_data = game_state.get("players", {})
        board_data = game_state.get("board", {})

        self._draw_stats(players_data)
        self._draw_board(board_data)

    def _draw_stats(self, players_data: dict) -> None:
        """Stampa le statistiche della partita in alto.

        Args:
            players_data (dict): Dati relativi ai giocatori.

        """
        self._console.print("\n[bold cyan]--- QUORIDOR - SPRINT 1 ---[/bold cyan]")

        # NOTA: Queste chiavi sono ipotetiche. Adattale al tuo Controller.
        turno = players_data.get("current_turn", "Sconosciuto")
        muri_p1 = players_data.get("p1_walls", 10)
        muri_p2 = players_data.get("p2_walls", 10)

        self._console.print(f"Turno di: [bold yellow]{turno}[/bold yellow]")

        # Spezzata la stringa per rispettare il limite di 88 caratteri
        self._console.print(
            f"Giocatore 1 (P1): {muri_p1} muri | Giocatore 2 (P2): {muri_p2} muri\n"
        )

    def _draw_board(self, board_data: dict) -> None:
        """Disegna la scacchiera 9x9 rispettando la Definition of Done.

        Args:
            board_data (dict): Dati con le posizioni di pedoni e muri.

        """
        table = Table(show_header=True, header_style="bold green", box=None)

        table.add_column(" ")

        for lettera in "abcdefghi":
            table.add_column(lettera, justify="center")

        for riga in range(1, 10):
            elementi_riga = [f"[bold green]{riga}[/bold green]"]

            # Usiamo '_' al posto di 'colonna' perché non usiamo la variabile
            for _ in range(9):
                cella = "."
                elementi_riga.append(cella)

            table.add_row(*elementi_riga)

        self._console.print(table)
        self._console.print()

    def get_input(self) -> str:
        """Richiede un comando testuale all'utente.

        Returns:
            str: La stringa inserita dal giocatore.

        """
        # Spezzata su due righe per evitare l'errore E501
        comando = self._console.input(
            "[bold magenta]Inserisci la tua mossa > [/bold magenta]"
        )
        return comando.strip().lower()

    def show_error(self, message: str) -> None:
        pass

    def show_victory(self, player_id: int) -> None:
        pass
