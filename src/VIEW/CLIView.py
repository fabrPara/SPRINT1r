"""Modulo per l'interfaccia a riga di comando (CLI) del gioco."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .BaseView import BaseView


class CLIView(BaseView):
    """Implementazione della View tramite Command Line Interface (CLI)."""

    def __init__(self):
        """Inizializza la CLI View creando un'istanza della Console di Rich."""
        self._console = Console()

    def render(self, game_state: dict) -> None:
        """Disegna lo stato completo del gioco aggiornato."""
        self._console.clear()

        # Mostra statistiche e turno
        self._draw_stats(game_state)

        # Recupera oggetti dal game_state
        board_obj = game_state.get("board")
        player_data = game_state.get("players", [])

        # Disegna la board solo se i dati sono validi
        if board_obj and player_data:
            self._draw_board(board_obj, player_data)

    def _draw_stats(self, game_state: dict):
        """Stampa le statistiche della partita."""
        self._console.print("\n[bold cyan]--- QUORIDOR - SPRINT 1 ---[/bold cyan]")

        turno = game_state.get("current_player_id", "?")
        players = game_state.get("players", [])

        if len(players) >= 2:
            # Assumiamo che gli oggetti Player abbiano il metodo get_walls_count()
            muri_p1 = players[0].get_walls_count()
            muri_p2 = players[1].get_walls_count()
            self._console.print(f"Turno di: [bold yellow]P{turno}[/bold yellow]")
            self._console.print(f"Muri P1: {muri_p1} | Muri P2: {muri_p2}")

    def _draw_board(self, board_obj, player_data: list) -> None:
        """Disegna la board con player e muri."""
        table = Table(
            show_header=False, show_edge=False, pad_edge=False, box=None, padding=0
        )

        # Configurazione delle 19 colonne (alternanza cella/spazio muro)
        for i in range(19):
            # Cella larga 7, Varco largo 1
            w = 7 if i > 0 and i % 2 != 0 else (1 if i > 0 else None)
            table.add_column(justify="center", width=w)

        # Recupero posizioni dei player
        p1_pos = player_data[0].get_position().get_coords()
        p2_pos = player_data[1].get_position().get_coords()

        # Recupero lista muri dall'oggetto Board
        muri = board_obj.get_walls()

        m_v, m_h = "[bold red]┃[/bold red]", "[bold red]━━━━━━━[/bold red]"
        m_c_v, m_c_h = "[bold red]┃[/bold red]", "[bold red]━[/bold red]"

        # 1. Riga intestazione lettere (a-i)
        c_let = [" "]
        for char in "abcdefghi":
            c_let.append(f"[bold green]{char}[/bold green]")
            if char != "i":
                c_let.append(" ")
        table.add_row(*c_let)

        # Trasformiamo i muri in una lista di tuple per facilitare il controllo
        # Formato: [((x, y), 'h'/'v'), ...]
        m_list = []
        for w in muri:
            p = w.get_start_cell()
            coords = p.get_coords() if hasattr(p, "get_coords") else (p.x, p.y)
            m_list.append((coords, w.get_orientation().lower()))

        # 2. Ciclo righe (1-9)
        for riga in range(1, 10):
            # Disegno dei muri orizzontali (se non siamo alla prima riga)
            if riga > 1:
                el_h = [" "]
                for c_h in range(1, 10):
                    # Un muro orizzontale in (x, riga-1) copre due celle
                    is_h = any(
                        o == "h" and c in [(c_h, riga - 1), (c_h - 1, riga - 1)]
                        for c, o in m_list
                    )
                    el_h.append(m_h if is_h else "       ")

                    if c_h < 9:
                        # Incrocio: mostra il muro verticale se passa di lì
                        v_h = any(o == "v" and c == (c_h, riga - 1) for c, o in m_list)
                        h_h = any(o == "h" and c == (c_h, riga - 1) for c, o in m_list)
                        el_h.append(m_c_v if v_h else (m_c_h if h_h else " "))
                table.add_row(*el_h)

            # Disegno celle e muri verticali
            el_riga = [f"[bold green]{riga}[/bold green]"]
            for col in range(1, 10):
                if (col, riga) == p1_pos:
                    cella = "[bold magenta][P1] [/bold magenta]"
                elif (col, riga) == p2_pos:
                    cella = "[bold cyan][P2]  [/bold cyan]"
                else:
                    cella = "[grey37][  ][/grey37]"
                el_riga.append(cella)

                if col < 9:
                    is_v = any(
                        o == "v" and c in [(col, riga), (col, riga - 1)]
                        for c, o in m_list
                    )
                    el_riga.append(m_v if is_v else " ")
            table.add_row(*el_riga)

        self._console.print(table)

    def get_input(self) -> str:
        """Richiede un comando all'utente."""
        return self._console.input(
            "\n[bold magenta]Inserisci la tua mossa > [/bold magenta]"
        ).strip()

    def show_error(self, message: str) -> None:
        """Mostra messaggi di errore."""
        self._console.print("-" * 20)
        self._console.print(f"[bold red]Attenzione: {message}[/bold red]")
        self._console.print("-" * 20)

    def show_victory(self, player_id: int) -> None:
        """Mostra il messaggio finale di vittoria."""
        victory_message = Panel(
            f"[bold green]🎉 GIOCATORE {player_id} HA VINTO! 🎉[/bold green]",
            style="bold green",
            expand=False,
        )
        self._console.print("\n")
        self._console.print(victory_message)
