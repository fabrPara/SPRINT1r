"""Modulo per l'interfaccia a riga di comando (CLI) del gioco."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.MODEL.Board import Board
from src.MODEL.Wall import Wall

from .BaseView import BaseView

# Colori associati a ciascun giocatore (indice = player_id - 1)
_PLAYER_COLORS = ["bold magenta", "bold cyan", "bold yellow", "bold green"]


def _player_color(player_id: int) -> str:
    """Restituisce il markup colore Rich per un dato player_id."""
    idx = (player_id - 1) % len(_PLAYER_COLORS)
    return _PLAYER_COLORS[idx]


class CLIView(BaseView):
    """Implementazione della View tramite Command Line Interface (CLI).

    Utilizza la libreria Rich per formattare l'output nel terminale.
    """

    def __init__(self) -> None:
        """Inizializza la CLI View creando un'istanza della Console di Rich."""
        self._console = Console()

    def render(self, game_state: dict) -> None:
        """Disegna lo stato completo del gioco aggiornato.

        Args:
            game_state (dict): Dizionario con lo stato del gioco.

        """
        self._console.clear()
        self._draw_stats(game_state)

        board_data = game_state.get("board", {})
        player_data = game_state.get("players", [])
        self._draw_board(board_data, player_data)

    def _draw_stats(self, game_state: dict) -> None:
        """Stampa le statistiche della partita inclusi i tempi rimanenti."""
        self._console.print("\n[bold cyan]--- QUORIDOR - SPRINT 1 ---[/bold cyan]")

        turno = game_state.get("current_player_id", 1)
        players = game_state.get("players", [])
        active_ids: list[int] = game_state.get(
            "active_player_ids", [p._id for p in players]
        )
        clocks: dict[int, float] = game_state.get("clocks", {})

        color = _player_color(turno)
        self._console.print(f"Turno di: [{color}]P{turno}[/{color}]")

        parts = []
        for p in players:
            pid = p._id
            walls = p._walls_count
            c = _player_color(pid)

            t_raw = clocks.get(pid, 99999.0)
            if t_raw >= 3600.0:
                tempo = "∞"
            else:
                tempo = f"{int(t_raw // 60)}m {int(t_raw % 60)}s"

            status = "" if pid in active_ids else " [dim](ritirato)[/dim]"
            parts.append(f"[{c}]P{pid}[/{c}]: {walls} muri ([clock] {tempo}){status}")

        self._console.print("  |  ".join(parts))

    # Sostituisci 'object' con 'Board'
    def _draw_board(self, board_data: Board, player_data: list) -> None:
        """Disegna la board con i giocatori."""
        table = Table(
            show_header=False, show_edge=False, pad_edge=False, box=None, padding=0
        )
        for i in range(19):
            w = 7 if i > 0 and i % 2 != 0 else (1 if i > 0 else None)
            table.add_column(justify="center", width=w)

        # Mappa posizione → etichetta giocatore
        pos_map: dict[tuple[int, int], str] = {}
        for p in player_data:
            coords = p._position.get_coords()
            color = _player_color(p._id)
            pos_map[coords] = f"[{color}][P{p._id}][/{color}] "

        muri = board_data.get_walls()

        m_v = "[bold red]┃[/bold red]"
        m_h = "[bold red]━━━━━━━[/bold red]"
        m_c_v = "[bold red]┃[/bold red]"
        m_c_h = "[bold red]━[/bold red]"

        # Sostituisci 'w: object' con 'w: Wall'
        def get_w_info(w: Wall) -> tuple[tuple[int, int], str]:
            p = w._start_cell
            c = p.get_coords() if hasattr(p, "get_coords") else p
            return c, w._orientation  # pyright: ignore[reportReturnType]

        # Intestazione colonne (lettere)
        c_let = [" "]
        for char in "abcdefghi":
            c_let.append(f"[bold green]{char}[/bold green]")
            if char != "i":
                c_let.append(" ")
        table.add_row(*c_let)

        m_list = [get_w_info(w) for w in muri]

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
                        v_h = any(
                            o == "v" and c in [(c_h + 1, riga), (c_h + 1, riga + 1)]
                            for c, o in m_list
                        )
                        h_h = any(o == "h" and c == (c_h, riga) for c, o in m_list)
                        el_h.append(m_c_v if v_h else (m_c_h if h_h else " "))
                table.add_row(*el_h)

            el_riga = [f"[bold green]{riga}[/bold green]"]
            for col in range(1, 10):
                label = pos_map.get((col, riga))
                if label:  # noqa: SIM108
                    cella = label
                else:
                    cella = "[grey37][  ][/grey37]"
                el_riga.append(cella)

                if col < 9:
                    is_v = any(
                        o == "v" and c in [(col + 1, riga), (col + 1, riga + 1)]
                        for c, o in m_list
                    )
                    el_riga.append(m_v if is_v else " ")
            table.add_row(*el_riga)

        self._console.print(table)

    def get_input(self) -> str:
        """Richiede un comando testuale all'utente."""
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
        color = _player_color(player_id)
        victory_message = Panel(
            f"[{color}]🎉 GIOCATORE {player_id} HA VINTO! 🎉[/{color}]",
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
In modalità 4 giocatori: P1→colonna 9, P2→colonna 1, P3→riga 9, P4→riga 1.

[bold yellow]MOVIMENTO[/bold yellow]
Muoviti di una sola cella alla volta verso qualsiasi direzione (su, giù,
sinistra, destra). Non puoi muoverti dove c'è un altro giocatore o attraverso
un muro.

[bold yellow]MURI[/bold yellow]
In 2 giocatori: 10 muri per giocatore.
In 4 giocatori: 5 muri per giocatore.
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

[bold green]abbandona[/bold green]            Abbandona la partita (o esci dal ciclo in 4P).
[bold green]exit[/bold green]                 Esci dal gioco.
[bold green]help[/bold green]                 Mostra questo messaggio.

[bold yellow]COORDINATE[/bold yellow]
Le colonne sono indicate con lettere (a-i), le righe con numeri (1-9).
I comandi sono case-insensitive (funzionano con maiuscole e minuscole).
Esempio: a1 è l'angolo in alto a sinistra, i9 è l'angolo in basso a destra.""",  # noqa: E501
            style="bold blue",
            expand=False,
        )
        self._console.print(help_panel)
        self._console.input(
            "\n[bold magenta]Premi Invio per tornare al gioco > [/bold magenta]"
        )

    def show_timeout(self, player_id: int) -> None:
        """Mostra il messaggio di tempo scaduto per il giocatore corrente."""
        self._console.print(
            f"\n[bold red]⌛ Tempo Scaduto! Il Giocatore P{player_id} "
            "ha esaurito i suoi minuti.[/bold red]"
        )

    def show_player_resigned(self, player_id: int) -> None:
        """Mostra il messaggio di abbandono in modalità 4P (partita continua)."""
        color = _player_color(player_id)
        self._console.print(
            f"\n[bold yellow]Il Giocatore [{color}]P{player_id}[/{color}] "
            "ha abbandonato. La partita continua tra i giocatori rimasti.[/bold yellow]"
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

    def prompt_game_settings(self) -> tuple[bool, float]:
        """Mostra il menu di configurazione della partita.

        Returns:
            tuple[bool, float]: (usa_tempo, secondi_totali)

        """
        self._console.clear()

        menu_text = (
            "[bold cyan]⚙️  IMPOSTAZIONI NUOVA PARTITA ⚙️[/bold cyan]\n\n"
            "Scegli la modalità di gioco:\n"
            "[bold green]1.[/bold green] Partita Classica (Senza Limite)\n"
            "[bold green]2.[/bold green] Partita Blitz (Orologio Scacchistico)"
        )
        self._console.print(Panel(menu_text, style="bold blue", expand=False))

        while True:
            scelta = self._console.input(
                "\n[bold magenta]Seleziona un'opzione (1 o 2) > [/bold magenta]"
            ).strip()

            if scelta == "1":
                return False, 0.0
            if scelta == "2":
                break
            self._console.print(
                "[bold red]Opzione non valida. Inserisci 1 o 2.[/bold red]"
            )

        while True:
            minuti_str = self._console.input(
                "\n[bold magenta]Inserisci i minuti per giocatore "
                "(Max 15) > [/bold magenta]"
            ).strip()

            if not minuti_str.isdigit():
                self._console.print(
                    "[bold red]Attenzione: Devi inserire un numero intero "
                    "valido![/bold red]"
                )
                continue

            minuti = int(minuti_str)
            if minuti < 1 or minuti > 15:
                self._console.print(
                    "[bold red]Attenzione: Il tempo deve essere compreso "
                    "tra 1 e 15 minuti![/bold red]"
                )
                continue

            return True, float(minuti * 60)

    def prompt_num_players(self) -> int:
        """Chiede quanti giocatori partecipano alla partita.

        Returns:
            int: 2 oppure 4.

        """
        self._console.print(
            Panel(
                "[bold cyan]Scegli la modalità:\n"
                "[bold green]1.[/bold green] 2 Giocatori\n"
                "[bold green]2.[/bold green] 4 Giocatori[/bold cyan]",
                style="bold blue",
                expand=False,
            )
        )
        while True:
            scelta = self._console.input(
                "\n[bold magenta]Seleziona (1 o 2) > [/bold magenta]"
            ).strip()
            if scelta == "1":
                return 2
            if scelta == "2":
                return 4
            self._console.print(
                "[bold red]Opzione non valida. Inserisci 1 o 2.[/bold red]"
            )
