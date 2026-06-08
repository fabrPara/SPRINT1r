"""Modulo per l'interfaccia utente testuale (TUI) del gioco via Textual."""

import contextlib
import threading
import time

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Header, Input, Label, RichLog, Static

from .BaseView import BaseView

# Colori associati a ciascun giocatore (markup standard per Textual/Rich)
_PLAYER_COLORS = ["magenta", "cyan", "yellow", "green"]


def _player_color(player_id: int) -> str:
    """Restituisce il colore associato a un determinato player_id."""
    idx = (player_id - 1) % len(_PLAYER_COLORS)
    return _PLAYER_COLORS[idx]


class SettingsScreen(Screen):
    """Schermata iniziale per la configurazione delle impostazioni."""

    CSS = (
        "SettingsScreen { align: center middle; background: #1a1a1a; }\n"
        "#settings-container { width: 50; height: auto; "
        "border: solid chromium; background: #262626; padding: 1 2; }\n"
        ".menu-title { text-align: center; text-style: bold; "
        "color: cyan; margin-bottom: 1; }\n"
        ".menu-label { margin-top: 1; margin-bottom: 0; "
        "text-style: bold; }\n"
        ".option-button { width: 100%; margin-bottom: 1; }\n"
    )

    def compose(self) -> ComposeResult:
        with Vertical(id="settings-container"):
            yield Label("⚙️ IMPOSTAZIONI QUORIDOR", classes="menu-title")
            
            yield Label("1. Seleziona Numero Giocatori:", classes="menu-label")
            yield Button(
                "2 Giocatori", id="btn-2p",
                variant="primary", classes="option-button"
            )
            yield Button(
                "4 Giocatori", id="btn-4p",
                variant="primary", classes="option-button"
            )
            
            yield Label("2. Seleziona Modalità di Gioco:", classes="menu-label")
            yield Button(
                "Partita Classica (Senza Limite)", id="btn-classic",
                variant="success", classes="option-button"
            )
            yield Button(
                "Partita Blitz (Orologio)", id="btn-blitz",
                variant="warning", classes="option-button"
            )


class PlayersScreen(Screen):
    """Schermata intermedia per configurare il tempo in modalità Blitz."""

    CSS = (
        "PlayersScreen { align: center middle; background: #1a1a1a; }\n"
        "#players-container { width: 50; height: auto; "
        "border: solid chromium; background: #262626; padding: 1 2; }\n"
        ".menu-title { text-align: center; text-style: bold; "
        "color: cyan; margin-bottom: 1; }\n"
        ".time-input { margin-bottom: 1; }\n"
    )

    def compose(self) -> ComposeResult:
        with Vertical(id="players-container"):
            yield Label("⌛ CONFIGURAZIONE TIMER BLITZ", classes="menu-title")
            yield Label("Inserisci i minuti per giocatore (1-15):")
            yield Input(
                placeholder="Esempio: 5", id="txt-minutes",
                classes="time-input"
            )
            yield Button(
                "Conferma e Inizia", id="btn-confirm-time",
                variant="success"
            )


class QuoridorTextualApp(App):
    """Applicazione Textual principale che gestisce il layout del gioco."""

    TITLE = "Quoridor TUI"
    BINDINGS = [
        ("h", "show_help", "Aiuto"),
        ("q", "quit", "Esci")
    ]

    CSS = (
        "Screen { background: #121212; }\n"
        "#main-layout { layout: horizontal; width: 100fr; height: 100fr; }\n"
        "#left-panel { width: 65fr; height: 100%; align: center middle; "
        "background: #181818; }\n"
        "#board-grid { layout: grid; grid-size: 19 19; width: auto; "
        "height: auto; padding: 1; }\n"
        ".cell { background: #242424; color: #777777; border: solid #3c3c3c; "
        "min-width: 5; height: 3; content-align: center middle; }\n"
        ".cell-player { text-style: bold; background: #333333; }\n"
        ".wall-h-active { background: red; }\n"
        ".wall-v-active { background: red; }\n"
        ".grid-label { color: #444444; text-style: bold; "
        "content-align: center middle; }\n"
        "#side-log { width: 35fr; height: 100%; background: #141414; "
        "border-left: solid #333; }\n"
        "#input-container { dock: bottom; layout: horizontal; height: 3; }\n"
        "#cmd-input { width: 80fr; }\n"
        "#btn-submit { width: 20fr; }\n"
    )

    def __init__(self, view: 'TUIView') -> None:
        super().__init__()
        self._view = view
        self._current_input_value = ""

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main-layout"):
            with Vertical(id="left-panel"):
                yield Container(id="board-grid")
                with Horizontal(id="input-container"):
                    yield Input(
                        placeholder="Mossa (es: e5, e5h, e5v)...",
                        id="cmd-input"
                    )
                    yield Button("Invia", id="btn-submit", variant="primary")
            yield RichLog(id="side-log", max_lines=1000, wrap=True)
        yield Footer()

    def on_mount(self) -> None:
        """Invocato all'avvio dell'applicazione."""
        self.call_later(self._view._on_app_ready)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Gestore centrale dei click sui bottoni di gioco."""
        btn_id = event.button.id
        
        if btn_id == "btn-2p":
            self._view._selected_players = 2
        elif btn_id == "btn-4p":
            self._view._selected_players = 4
        elif btn_id == "btn-classic":
            self._view._use_time = False
            self._view._total_seconds = 0.0
            self.pop_screen()
        elif btn_id == "btn-blitz":
            self.push_screen(PlayersScreen())
        elif btn_id == "btn-confirm-time":
            txt_input = self.query_one("#txt-minutes", Input)
            val = txt_input.value.strip()
            if val.isdigit() and 1 <= int(val) <= 15:
                self._view._use_time = True
                self._view._total_seconds = float(int(val) * 60)
                self.pop_screen()
                self.pop_screen()
            else:
                txt_input.value = ""
                txt_input.placeholder = "Minuti non validi (1-15):"
        elif btn_id == "btn-submit":
            self._process_command()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Permette l'invio del comando premendo il tasto Invio."""
        if event.input.id == "cmd-input":
            self._process_command()

    def _process_command(self) -> None:
        """Salva il testo dall'input e sblocca l'attesa."""
        inp = self.query_one("#cmd-input", Input)
        cmd = inp.value.strip()
        if cmd:
            self._current_input_value = cmd
            inp.value = ""
            self._view._release_input_wait()


class TUIView(BaseView):
    """Implementazione della View tramite Textual User Interface (TUI)."""

    def __init__(self) -> None:
        self._app = QuoridorTextualApp(self)
        self._selected_players = 2
        self._use_time = False
        self._total_seconds = 0.0
        self._input_event = threading.Event()

    def _on_app_ready(self) -> None:
        self.show_initial_message()

    def _release_input_wait(self) -> None:
        self._input_event.set()

    def render(self, game_state: dict) -> None:
        if not self._app.is_running:
            return
        self._app.call_from_thread(self._sync_render, game_state)

    def _sync_render(self, game_state: dict) -> None:
        """Sincronizza i componenti grafici interni con il game_state."""
        try:
            grid = self._app.query_one("#board-grid", Container)
        except Exception:
            return

        grid.query("*").remove()

        board_data = game_state.get("board", {})
        player_data = game_state.get("players", [])
        
        muri_piazzati = (
            board_data.get_walls()
            if hasattr(board_data, "get_walls") else []
        )

        pos_map = {}
        for p in player_data:
            coords = p._position.get_coords()
            pos_map[coords] = p._id

        m_list = []
        for w in muri_piazzati:
            p = w._start_cell
            c = p.get_coords() if hasattr(p, "get_coords") else p
            m_list.append((c, w._orientation))

        grid.yield_with_checks(Static("", classes="grid-label"))
        for char in "abcdefghi":
            grid.yield_with_checks(Static(char.upper(), classes="grid-label"))
            if char != "i":
                grid.yield_with_checks(Static("", classes="grid-label"))
        grid.yield_with_checks(Static("", classes="grid-label"))

        for riga_logica in range(1, 10):
            if riga_logica > 1:
                grid.yield_with_checks(Static("", classes="grid-label"))
                for col_logica in range(1, 10):
                    is_h = any(
                        o == "h" and c in [
                            (col_logica, riga_logica),
                            (col_logica - 1, riga_logica)
                        ] for c, o in m_list
                    )
                    cl_h = "wall-h-active" if is_h else "cell-wall-h"
                    grid.yield_with_checks(
                        Static("━━━━━" if is_h else "", classes=cl_h)
                    )

                    if col_logica < 9:
                        grid.yield_with_checks(
                            Static("", classes="cell-intersection")
                        )
                grid.yield_with_checks(Static("", classes="grid-label"))

            grid.yield_with_checks(
                Static(str(riga_logica), classes="grid-label")
            )
            for col_logica in range(1, 10):
                pid = pos_map.get((col_logica, riga_logica))
                if pid:
                    color = _player_color(pid)
                    cell_widget = Static(f"P{pid}", classes="cell cell-player")
                    cell_widget.styles.color = color
                else:
                    cell_widget = Static("[ ]", classes="cell")
                grid.yield_with_checks(cell_widget)

                if col_logica < 9:
                    is_v = any(
                        o == "v" and c in [
                            (col_logica + 1, riga_logica),
                            (col_logica + 1, riga_logica + 1)
                        ] for c, o in m_list
                    )
                    cl_v = "wall-v-active" if is_v else "cell-wall-v"
                    grid.yield_with_checks(
                        Static("┃" if is_v else "", classes=cl_v)
                    )
            grid.yield_with_checks(
                Static(str(riga_logica), classes="grid-label")
            )

        log = self._app.query_one("#side-log", RichLog)
        log.clear()
        
        turno = game_state.get("current_player_id", 1)
        log.write(
            f"[bold cyan]🔄 TURNO CORRENTE: Giocatore P{turno}[/bold cyan]\n"
        )
        log.write("-" * 30)
        
        clocks = game_state.get("clocks", {})
        active_ids = game_state.get(
            "active_player_ids", [p._id for p in player_data]
        )

        for p in player_data:
            c = _player_color(p._id)
            t_raw = clocks.get(p._id, 99999.0)
            tempo = (
                "∞" if t_raw >= 3600.0 else
                f"{int(t_raw // 60)}m {int(t_raw % 60)}s"
            )
            status = "" if p._id in active_ids else " [dim](ritirato)[/dim]"
            
            log.write(f"[{c}]● Giocatore P{p._id}[/{c}]:")
            log.write(f"  Muri disponibili: [bold]{p._walls_count}[/bold]")
            log.write(f"  Tempo residuo: {tempo}{status}\n")

    def get_input(self) -> str:
        """Blocca il thread in attesa dell'input da TUI."""
        self._input_event.clear()
        self._input_event.wait()
        return self._app._current_input_value.strip().lower()

    def _write_to_log(self, text: str) -> None:
        """Scrive in modo thread-safe."""
        with contextlib.suppress(Exception):
            self._app.query_one("#side-log", RichLog).write(text)

    # =========================================================================
    # OVERRIDE METODI REALI DA BASEVIEW
    # =========================================================================

    def show_error(self, message: str) -> None:
        if self._app.is_running:
            self._app.call_from_thread(
                self._write_to_log, f"[bold red]❌ Errore: {message}[/bold red]"
            )

    def show_victory(self, player_id: int) -> None:
        if self._app.is_running:
            msg = (
                f"\n[bold green]🎉 GIOCATORE {player_id} "
                "HA VINTO LA PARTITA! 🎉[/bold green]"
            )
            self._app.call_from_thread(self._write_to_log, msg)

    def show_initial_message(self) -> None:
        if self._app.is_running:
            msg = "[bold green]Benvenuto su Quoridor TUI![/bold green]\n"
            self._app.call_from_thread(self._write_to_log, msg)

    def show_help(self) -> None:
        if self._app.is_running:
            msg = (
                "\n[bold yellow]💡 GUIDA COMANDI:[/bold yellow]\n"
                "• Per muoverti: scrivi la cella (es: e2)\n"
                "• Per i muri: aggiungi h o v (es: e2h, e2v)"
            )
            self._app.call_from_thread(self._write_to_log, msg)

    def show_exit(self, winner_id: int) -> None:
        if self._app.is_running:
            msg = (
                f"\n[bold red]Gioco Interrotto. "
                f"Vince P{winner_id}![/bold red]"
            )
            self._app.call_from_thread(self._write_to_log, msg)

    def show_exit_message(self) -> None:
        if self._app.is_running:
            msg = "[bold yellow]Chiusura del gioco in corso...[/bold yellow]"
            self._app.call_from_thread(self._write_to_log, msg)

    def show_timeout(self, player_id: int) -> None:
        if self._app.is_running:
            msg = (
                f"\n[bold red]⌛ Tempo scaduto per il "
                f"Giocatore P{player_id}![/bold red]"
            )
            self._app.call_from_thread(self._write_to_log, msg)

    def show_player_resigned(self, player_id: int) -> None:
        if self._app.is_running:
            msg = (
                f"\n[bold orange3]🏳️ Il Giocatore P{player_id} "
                "si è ritirato.[/bold orange3]"
            )
            self._app.call_from_thread(self._write_to_log, msg)

    def show_move_history(
        self, move_history: list[dict], num_players: int
    ) -> None:
        if self._app.is_running:
            title = (
                "\n[bold underline]"
                "CRONOLOGIA MOSSE:"
                "[/bold underline]"
            )
            self._app.call_from_thread(self._write_to_log, title)
            for idx, mossa in enumerate(move_history):
                turno = (idx // num_players) + 1
                pid = mossa.get("player_id", "?")
                notat = mossa.get("notation", "")
                msg = f"Turno {turno} -> P{pid}: {notat}"
                self._app.call_from_thread(self._write_to_log, msg)

    # =========================================================================
    # METODI DI PROMPT INTERATTIVI E CONFIGURAZIONE
    # =========================================================================

    def prompt_new_game(self) -> str:
        return "n"

    def prompt_replay(self) -> str:
        return "n"

    def prompt_num_players(self) -> int:
        """Avvia l'app e attende finché non è completamente inizializzata."""
        if not self._app.is_running:
            threading.Thread(target=self._app.run, daemon=True).start()
        
        while not self._app.is_running:
            time.sleep(0.05)
            
        self._app.call_from_thread(self._app.push_screen, SettingsScreen())
        return self._selected_players

    def prompt_game_settings(self) -> tuple[bool, float]:
        return self._use_time, self._total_seconds