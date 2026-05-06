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

        turno = players_data.get("current_turn", "Sconosciuto")
        muri_p1 = players_data.get("p1_walls", 10)
        muri_p2 = players_data.get("p2_walls", 10)

        self._console.print(f"Turno di: [bold yellow]{turno}[/bold yellow]")

        # Spezzata la stringa per rispettare il limite di 88 caratteri di Ruff
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

        # Estraiamo le posizioni correnti dai dati della board.
        # Supponiamo siano salvate come tuple (x, y).
        # (5, 1) è la partenza standard di P1 in Quoridor (e1)
        # (5, 9) è la partenza standard di P2 in Quoridor (e9)
        p1_pos = board_data.get("p1_pos", (5, 1))
        p2_pos = board_data.get("p2_pos", (5, 9))

        for riga in range(1, 10):
            elementi_riga = [f"[bold green]{riga}[/bold green]"]

            for col in range(9):
                x = col + 1  # La colonna 'a' è 1, 'b' è 2, ecc.
                y = riga  # La riga va da 1 a 9

                cella = "[grey37].[/grey37]"

                # Inserisce dinamicamente P1 o P2 se la coordinata coincide
                if (x, y) == p1_pos:
                    cella = "[bold magenta]P1[/bold magenta]"
                elif (x, y) == p2_pos:
                    cella = "[bold cyan]P2[/bold cyan]"

                elementi_riga.append(cella)

            table.add_row(*elementi_riga)

        self._console.print(table)
        self._console.print()

    def get_input(self) -> str:
        """Richiede un comando testuale all'utente.

        Returns:
            str: La stringa inserita dal giocatore.

        """
        comando = self._console.input(
            "[bold magenta]Inserisci la tua mossa > [/bold magenta]"
        )
        return comando.strip().lower()

    def show_error(self, message: str) -> None:
        pass

    def show_victory(self, player_id: int) -> None:
        pass
