"""Modulo per l'interfaccia a riga di comando (CLI) del gioco."""

from rich.console import Console
from rich.panel import Panel
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
        """Stampa le statistiche della partita come il turno attuale e i muri rimanenti.

        Args:
            players_data (dict): _description_

        """
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
            c = p.get_coords() if hasattr(p, "get_coords") else p
            return c, w._orientation

        # 1. COORDINATE LETTERE
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
                        o == "h" and c in [(c_h, riga), (c_h - 1, riga)]
                        for c, o in m_list
                    )
                    el_h.append(m_h if is_h else "       ")
                    if c_h < 9:
                        # Intersezione: un incrocio è occupato se c'è un muro H
                        # o se un muro V passa da lì (attivato a riga o riga+1)
                        v_h = any(
                            o == "v" and c in [(c_h + 1, riga), (c_h + 1, riga + 1)]
                            for c, o in m_list
                        )
                        h_h = any(o == "h" and c == (c_h, riga) for c, o in m_list)
                        el_h.append(m_c_v if v_h else (m_c_h if h_h else " "))
                table.add_row(*el_h)

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
                    # Il muro verticale in col+1 attivato a riga o riga+1
                    # sale e si estende sulla riga corrente
                    is_v = any(
                        o == "v" and c in [(col + 1, riga), (col + 1, riga + 1)]
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

    def show_exit(self, winner_id: int) -> None:
        """Mostra il messaggio di uscita dalla partita e il vincitore."""
        self._console.print(
            "\n[bold yellow]Hai abbandonato la partita. "
            f"Di conseguenza il giocatore P{winner_id} ha vinto![/bold yellow]"
        )

    def show_exit_message(self) -> None:
        """Mostra il messaggio quando l'utente esce dal gioco."""
        exit_message = Panel(
            "[bold cyan]Hai scelto di uscire dal gioco.\nAlla prossima![/bold cyan]",
            style="bold cyan",
            expand=False,
        )
        self._console.print("\n")
        self._console.print(exit_message)

    def show_initial_message(self) -> None:
        """Mostra il messaggio iniziale con istruzioni."""
        self._console.print("\n")
        self._console.print(
            '[bold cyan]Digita "help" per visualizzare le regole del gioco '
            "e i comandi per muoverti e piazzare i muri.[/bold cyan]"
        )
        self._console.print(
            '[bold cyan]Digita "exit" per uscire dal gioco.[/bold cyan]'
        )
        self._console.print("\n")

    def show_help(self) -> None:
        """Mostra l'help con le regole e i comandi del gioco."""
        self._console.clear()
        help_panel = Panel(
            """[bold cyan]REGOLE DEL GIOCO QUORIDOR[/bold cyan]

[bold yellow]OBIETTIVO[/bold yellow]
Raggiungi il lato opposto della scacchiera prima del tuo avversario.
Il giocatore 1 deve raggiungere la riga 9, il giocatore 2 la riga 1.

[bold yellow]MOVIMENTO[/bold yellow]
Muoviti di una sola cella alla volta verso qualsiasi direzione (su, giù,
sinistra, destra). Non puoi muoverti dove c'è un altro giocatore o attraverso
un muro.

[bold yellow]MURI[/bold yellow]
Possiedi 10 muri per il resto della partita. Usa i muri per bloccare l'avversario.
I muri possono essere piazzati orizzontalmente o verticalmente e occupano due celle.
Non puoi piazzare:
  • Muri fuori dalla scacchiera
  • Muri sovrapposti
  • Muri che formano una croce

[bold yellow]COMANDI[/bold yellow]
[bold green]<cella>[/bold green]             Muovi il pedone. Es: e5 oppure E5

[bold green]<cella>h[/bold green]            Piazza un muro orizzontale.
                      Es: e5h oppure E5H

[bold green]<cella>v[/bold green]            Piazza un muro verticale.
                      Es: e5v oppure E5V

[bold green]abbandona[/bold green]            Abbandona la partita.
[bold green]exit[/bold green]                 Esci dal gioco.
[bold green]help[/bold green]                 Mostra questo messaggio.

[bold yellow]COORDINATE[/bold yellow]
Le colonne sono indicate con lettere (a-i), le righe con numeri (1-9).
I comandi sono case-insensitive (funzionano con maiuscole e minuscole).
Esempio: a1 è l'angolo in alto a sinistra, i9 è l'angolo in basso a destra.""",
            style="bold blue",
            expand=False,
        )
        self._console.print(help_panel)
        self._console.input(
            "\n[bold magenta]Premi Invio per tornare al gioco > [/bold magenta]"
        )

    def prompt_new_game(self) -> str:
        """Chiede all'utente se vuole iniziare una nuova partita."""
        response = (
            self._console.input(
                "\n[bold yellow]Desideri iniziarne un'altra? (Si = s, No = n) > "
                "[/bold yellow]"
            )
            .strip()
            .lower()
        )
        return response