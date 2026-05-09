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

        self._draw_stats(game_state)

        board_data = game_state.get("board", {})
        player_data = game_state.get("players", [])
        self._draw_board(board_data, player_data)

    def _draw_stats(self, players_data: dict):
        self._console.print("\n[bold cyan]--- QUORIDOR - SPRINT 1 ---[/bold cyan]")

        turno = players_data.get("current_player_id", [])
        muri_p1 = players_data.get("players", [])[0]._walls_count
        muri_p2 = players_data.get("players", [])[1]._walls_count

        self._console.print(f"Turno di: [bold yellow]P{turno}[/bold yellow]")
        self._console.print(f"Muri P1: {muri_p1} | Muri P2: {muri_p2}")

    def _draw_board(self, board_data: dict, player_data: list) -> None:
        """Disegna la board con player ."""
        table = Table(
            show_header=False, show_edge=False, pad_edge=False, box=None, padding=0
        )
        for i in range(19):
            # 1=varchi/muri V, 7=celle/muri H
            w = 7 if i > 0 and i % 2 != 0 else (1 if i > 0 else None)
            table.add_column(justify="center", width=w)

        p1_pos = player_data[0]._position.get_coords()
        p2_pos = player_data[1]._position.get_coords()
        muri = board_data.get_walls()

        m_v, m_h = "[bold red]┃[/bold red]", "[bold red]━━━━━━━[/bold red]"
        m_c_v, m_c_h = "[bold red]┃[/bold red]", "[bold red]━[/bold red]"

        def get_w_info(w):
            p = w._start_cell
            c = p.get_coords() if hasattr(p, "get_coords") else (p.x, p.y)

            orient = w._orientation.upper()

            if orient == "H":
                return (c[0] + 1, c[1] + 2), orient
            else:
                return (c[0] + 2, c[1] + 3), orient

        # 1. COORDINATE LETTERE (Allineamento corretto: 4 spazi + lettera + 2 spazi)
        c_let = [" "]
        for char in "abcdefghi":
            c_let.append(f"[bold green]{char}[/bold green]")
            if char != "i":
                c_let.append(" ")
        table.add_row(*c_let)

        m_list = [get_w_info(w) for w in muri]

        # 2. CICLO RIGHE
        for riga in range(1, 10):
            if riga > 1:
                el_h = [" "]
                for c_h in range(1, 10):
                    is_h = any(
                        o == "H" and c in [(c_h, riga), (c_h - 1, riga)]
                        for c, o in m_list
                    )
                    el_h.append(m_h if is_h else "       ")
                    if c_h < 9:
                        v_h = any(
                            o == "V" and c in [(c_h + 1, riga), (c_h + 1, riga + 1)]
                            for c, o in m_list
                        )
                        h_h = any(o == "H" and c == (c_h, riga) for c, o in m_list)
                        el_h.append(m_c_v if v_h else (m_c_h if h_h else " "))
                table.add_row(*el_h)

            el_riga = [f"[bold green]{riga}[/bold green]"]
            for col in range(1, 10):
                # Rimosse le quadre dai player per evitare che la cella si allarghi
                if (col, riga) == p1_pos:
                    cella = "[bold magenta][P1] [/bold magenta]"
                elif (col, riga) == p2_pos:
                    cella = "[bold cyan][P2]  [/bold cyan]"
                else:
                    cella = "[grey37][  ][/grey37]"
                el_riga.append(cella)

                if col < 9:
                    is_v = any(
                        o == "V" and c in [(col + 1, riga + 1), (col + 1, riga + 2)]
                        for c, o in m_list
                    )
                    el_riga.append(m_v if is_v else " ")
            table.add_row(*el_riga)

        self._console.print(table)

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
