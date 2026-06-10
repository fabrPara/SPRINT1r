import contextlib
from typing import Any

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.events import Enter, Leave
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Input, RichLog, Static

ASCII_TITLE = """[bold orange3]
 ██████  ██    ██  ██████  ██████  ██ ██████   ██████  ██████  
██    ██ ██    ██ ██    ██ ██   ██ ██ ██   ██ ██    ██ ██   ██ 
██    ██ ██    ██ ██    ██ ██████  ██ ██   ██ ██    ██ ██████  
██ ▄▄ ██ ██    ██ ██    ██ ██   ██ ██ ██   ██ ██    ██ ██████  
 ██████   ██████   ██████  ██   ██ ██ ██████   ██████  ██   ██ 
    ▀▀                                                         
[/bold orange3]"""


class MoveRequested(Message):
    """Messaggio emesso quando l'utente richiede un movimento."""

    def __init__(self, cell_id: str) -> None:
        super().__init__()
        self.cell_id = cell_id


class WallPlacementRequested(Message):
    """Messaggio emesso per richiedere il piazzamento di un muro."""

    def __init__(self, orientation: str, anchor: str) -> None:
        super().__init__()
        self.orientation = orientation
        self.anchor = anchor


class ReplayActionRequested(Message):
    """Messaggio per i controlli di riproduzione dello storico."""

    def __init__(self, action: str) -> None:
        super().__init__()
        self.action = action


class ExitRequested(Message):
    """Messaggio emesso per chiudere l'applicazione."""


class ShowHistoryRequested(Message):
    """Messaggio emesso per visualizzare la cronologia."""


class HelpRequested(Message):
    """Messaggio emesso per richiedere la guida di gioco."""


class ResignRequested(Message):
    """Messaggio emesso quando un giocatore abbandona."""


class GridNode(Static):
    """Nodo interattivo della scacchiera."""

    def __init__(self, r: int, c: int) -> None:
        super().__init__(" ")
        self.grid_r = r
        self.grid_c = c

        if r % 2 == 0 and c % 2 == 0:
            self.add_class("board-cell")
        elif r % 2 == 1 and c % 2 == 1:
            self.add_class("intersection")
        else:
            self.add_class("wall-slot")

    def on_enter(self, event: Enter) -> None:  # type: ignore[override]
        if self.has_class("wall-slot") and hasattr(self.app, "highlight_wall"):
            self.app.highlight_wall(self.grid_r, self.grid_c, show=True)

    def on_leave(self, event: Leave) -> None:  # type: ignore[override]
        if self.has_class("wall-slot") and hasattr(self.app, "highlight_wall"):
            self.app.highlight_wall(self.grid_r, self.grid_c, show=False)

    def on_click(self) -> None:  # type: ignore[override]
        if self.has_class("board-cell"):
            logical_r = self.grid_r // 2
            logical_c = self.grid_c // 2
            cell_id = f"{chr(ord('a') + logical_c)}{logical_r + 1}"
            self.post_message(MoveRequested(cell_id))
            return

        if self.has_class("wall-slot"):
            if self.grid_r % 2 == 1 and self.grid_c % 2 == 0:
                orientation = "h"
                anchor_r = self.grid_r // 2
                anchor_c = self.grid_c // 2
            else:
                orientation = "v"
                anchor_r = self.grid_r // 2
                anchor_c = self.grid_c // 2

            anchor = f"{chr(ord('a') + anchor_c)}{anchor_r + 1}"
            self.post_message(WallPlacementRequested(orientation, anchor))


class PlayerSelectionScreen(ModalScreen):
    """Schermata modale per selezionare 2 o 4 giocatori."""

    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Static(ASCII_TITLE, id="ascii_art")
            yield Static("Seleziona numero giocatori", id="modal_title")
            with Horizontal(id="modal_buttons"):
                yield Button("2 Giocatori", id="btn_2players", variant="primary")
                yield Button("4 Giocatori", id="btn_4players", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:  # type: ignore[override]
        if event.button.id == "btn_2players":
            self.dismiss({"num_players": 2})
        elif event.button.id == "btn_4players":
            self.dismiss({"num_players": 4})


class TimeSettingsScreen(ModalScreen):
    """Schermata modale per impostare il timer della partita."""

    def __init__(self) -> None:
        super().__init__()
        self._blitz_mode = False

    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Static(ASCII_TITLE, id="ascii_art")
            yield Static("Impostazioni tempo di gioco", id="modal_title")
            with Horizontal(id="modal_buttons"):
                yield Button("Partita Classica", id="btn_classica", variant="success")
                yield Button("Partita Blitz", id="btn_blitz", variant="warning")
            
            with Vertical(id="blitz_container", classes="hidden"):
                yield Static(
                    "Inserisci i minuti per Blitz (1-15):", id="minutes_label"
                )
                yield Input(placeholder="es. 5", id="minutes_input")
                yield Button("Conferma", id="btn_confirm_blitz", variant="primary")
                yield Static("", id="time_error", classes="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:  # type: ignore[override]
        if event.button.id == "btn_classica":
            self.dismiss({"use_time": False, "minutes": 0})
            return

        if event.button.id == "btn_blitz":
            self._blitz_mode = True
            self.query_one("#blitz_container", Vertical).remove_class("hidden")
            return

        if event.button.id == "btn_confirm_blitz":
            minutes_input = self.query_one("#minutes_input", Input)
            value = minutes_input.value.strip()
            try:
                minutes = int(value)
                if minutes < 1 or minutes > 15:
                    raise ValueError
            except Exception:
                self.query_one("#time_error", Static).update(
                    "[red]Inserisci un numero valido tra 1 e 15.[/red]"
                )
                return

            self.dismiss({"use_time": True, "minutes": minutes})

    def on_input_changed(self, event: Input.Changed) -> None:  # type: ignore[override]
        if event.input.id == "minutes_input":
            self.query_one("#time_error", Static).update("")


class EndGameScreen(ModalScreen):
    """Schermata modale mostrata a fine partita."""

    def __init__(self, message: str) -> None:
        super().__init__()
        self._message = message

    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            yield Static(ASCII_TITLE, id="ascii_art")
            yield Static(self._message, id="modal_title")
            with Horizontal(id="modal_buttons"):
                yield Button("Nuova Partita", id="btn_new_game", variant="success")
                yield Button("Guarda Replay", id="btn_watch_replay", variant="primary")
                yield Button("Esci dal Gioco", id="btn_quit", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:  # type: ignore[override]
        if event.button.id == "btn_new_game":
            self.dismiss({"action": "new_game"})
        elif event.button.id == "btn_watch_replay":
            self.dismiss({"action": "replay"})
        elif event.button.id == "btn_quit":
            self.dismiss({"action": "quit"})


class AdvancedView(App):
    """Vista principale Textual con layout e logica per Quoridor."""

    CSS = """
    ModalScreen { align: center middle; background: $background 80%; }

    #dialog {
        width: auto; height: auto; padding: 2 4;
        border: thick $primary; background: $surface; align: center middle;
    }

    #ascii_art { text-align: center; margin-bottom: 2; }
    #modal_title { text-align: center; text-style: bold; margin-bottom: 1; }
    #modal_buttons { layout: horizontal; align: center middle; height: auto; }
    #modal_buttons Button { margin: 0 1; }
    
    #blitz_container { 
        align: center middle; 
        margin-top: 2; 
        height: auto; 
        width: 100%; 
    }
    
    #minutes_input { width: 20; margin: 1 0; }
    #time_error { margin-top: 1; }
    
    #root-header { 
        height: 3; 
        content-align: center middle; 
        background: $surface; 
        color: $text; 
        border: heavy $accent; 
    }
    
    #main { height: auto; padding: 1; }
    
    #left-pane {
        width: 66%; 
        height: 1fr; 
        align: center middle; 
        padding: 1; 
        overflow-y: auto;
    }

    #board-frame {
        border: heavy $accent; 
        padding: 0; 
        background: $panel; 
        width: auto; 
        height: auto;
    }

    #board {
        layout: grid;
        grid-size: 17 17;
        grid-columns: 4 2 4 2 4 2 4 2 4 2 4 2 4 2 4 2 4;
        grid-rows: 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2 1 2;
        width: 52;
        height: 26;
        grid-gutter: 0;
        margin: 1;
    }

    GridNode { width: 100%; height: 100%; }

    .board-cell { background: #f3e9db; content-align: center middle; }
    .board-cell:hover { background: #ffffff; }
    .wall-slot { background: transparent; }
    .intersection { background: transparent; }
    .hidden { display: none; }

    .pawn-p1 { color: red; }
    .pawn-p2 { color: blue; }
    .pawn-p3 { color: green; }
    .pawn-p4 { color: yellow; }

    /* Muri fantasma in semitrasparenza chiara */
    .ghost-wall { background: #FFCC80; }
    
    /* Muri posizionati */
    .wall-p1, .wall-p2, .wall-p3, .wall-p4 { 
        background: #FF8C00; 
    }

    #sidebar { width: 34%; height: 1fr; padding: 1; background: $surface; }
    #players_info { 
        border: round $primary; 
        height: auto; 
        padding: 1; 
        margin-bottom: 1; 
    }
    #action_buttons { 
        layout: grid; 
        grid-size: 2 2; 
        grid-gutter: 1; 
        margin: 1 0; 
    }
    #action_buttons Button { width: 100%; }
    #move_log { height: 1fr; overflow-y: scroll; }
    #root-footer { height: 1; }
    """

    BINDINGS = [
        ("left", "replay_prev", "Replay Prev"),
        ("right", "replay_next", "Replay Next"),
        ("space", "replay_toggle", "Replay Toggle"),
        ("escape", "exit_app", "Exit"),
    ]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.controller: Any = None
        self._selected_num_players: int = 2
        self._is_timed_game: bool = False
        self._default_minutes: int = 0
        self._timer_handle: Any = None
        self._menu_completed: bool = False
        self._victory_shown: bool = False
        
        # Stato del Replay
        self._in_replay_mode: bool = False
        self._replay_step: int = 0
        self._replay_max: int = 0
        self._replay_timer: Any = None

    def highlight_wall(self, grid_r: int, grid_c: int, show: bool) -> None:
        """Aggiunge o rimuove l'effetto hover per il muro fantasma."""
        nodes = []
        if grid_r % 2 == 1 and grid_c % 2 == 0:
            if grid_c > 14:
                return
            nodes = [(grid_r, grid_c), (grid_r, grid_c + 1), (grid_r, grid_c + 2)]
        elif grid_r % 2 == 0 and grid_c % 2 == 1:
            if grid_r > 14:
                return
            nodes = [(grid_r, grid_c), (grid_r + 1, grid_c), (grid_r + 2, grid_c)]
        else:
            return

        for node in self.query("GridNode"):
            if (node.grid_r, node.grid_c) in nodes:
                is_occupied = any(node.has_class(f"wall-p{i}") for i in range(1, 5))
                if show and not is_occupied:
                    node.add_class("ghost-wall")
                elif not show:
                    node.remove_class("ghost-wall")

    def compose(self) -> ComposeResult:
        yield Static("", id="root-header")
        with Horizontal(id="main"):
            with Container(id="left-pane"), Container(id="board-frame"), Container(
                id="board"
            ):
                for r in range(17):
                    for c in range(17):
                        yield GridNode(r, c)

            with Vertical(id="sidebar"):
                with Container(id="players_info", classes="panel"):
                    yield Static("Players", id="players_title")
                    yield Static("", id="players_status", markup=True)

                with Container(id="action_buttons"):
                    yield Button("📜 Storico", id="btn_storico")
                    yield Button("❓ Aiuto", id="btn_aiuto", variant="primary")
                    yield Button("🏳️ Resa", id="btn_abbandona", variant="warning")
                    yield Button("❌ Esci", id="btn_esci", variant="error")

                with Container(id="log_block"):
                    yield RichLog(id="move_log", markup=True)
                    with Horizontal(id="replay_controls"):
                        yield Button("⏪", id="btn_prev")
                        yield Button("▶️", id="btn_toggle")
                        yield Button("⏩", id="btn_next")

        yield Footer(id="root-footer")

    def on_mount(self) -> None:
        self.show_initial_message()
        self.push_screen(
            PlayerSelectionScreen(), callback=self._on_player_selection_done
        )

    def _on_player_selection_done(self, result: Any) -> None:
        if not isinstance(result, dict):
            return
        self._selected_num_players = int(result.get("num_players", 2))
        self.push_screen(TimeSettingsScreen(), callback=self._on_time_settings_done)

    def _on_time_settings_done(self, result: Any) -> None:
        if not isinstance(result, dict):
            return
        self._is_timed_game = bool(result.get("use_time", False))
        self._default_minutes = int(result.get("minutes", 0))
        self._configure_game()

    def _configure_game(self) -> None:
        if not self.controller or not hasattr(self.controller, "_model"):
            self.add_log_entry("[red]Controller non definito: errore critico.[/red]")
            return

        self._victory_shown = False
        self._in_replay_mode = False
        self._replay_pause()
        
        # Ripristina l'etichetta del bottone Resa per la nuova partita
        with contextlib.suppress(Exception):
            btn = self.query_one("#btn_abbandona", Button)
            btn.label = "🏳️ Resa"
            btn.variant = "warning"
        
        self.controller._model.reset(self._selected_num_players)
        self.controller._is_timed_game = self._is_timed_game
        self.controller._default_time_seconds = (
            float(self._default_minutes * 60) if self._is_timed_game else 99999.0
        )

        game_state = self.controller._model.get_game_state()
        players = game_state.get("players", [])
        
        player_ids = []
        for p in players:
            if isinstance(p, dict):
                player_ids.append(p.get("_id"))
            else:
                player_ids.append(getattr(p, "_id", None))
        
        player_ids = [pid for pid in player_ids if pid is not None]
        if not player_ids:
            player_ids = [1, 2] if self._selected_num_players == 2 else [1, 2, 3, 4]

        self.controller._players_clocks = {
            pid: self.controller._default_time_seconds for pid in player_ids
        }
        self._menu_completed = True
        self.render(self.controller._model.get_game_state())
        self._start_timer()

    def _set_game_over_state(self) -> None:
        """Blocca il gioco e trasforma il pulsante di resa in un menu."""
        self._victory_shown = True
        if self._timer_handle:
            self._timer_handle.pause()
        with contextlib.suppress(Exception):
            btn = self.query_one("#btn_abbandona", Button)
            btn.label = "🔙 Menu"
            btn.variant = "primary"

    def _start_timer(self) -> None:
        if self._timer_handle is None:
            self._timer_handle = self.set_interval(1.0, self._tick_timer)
        else:
            self._timer_handle.resume()

    def _tick_timer(self) -> None:
        if not self.controller or not getattr(
            self.controller, "_is_timed_game", False
        ):
            return

        game_state = self.controller._model.get_game_state()
        has_winner = game_state.get("winner") is not None
        if has_winner or self.controller._model.check_victory():
            if self._timer_handle:
                self._timer_handle.pause()
            return

        current_player_id = game_state.get("current_player_id")
        if current_player_id is None:
            return

        current_clock = self.controller._players_clocks.get(current_player_id)
        if current_clock is None:
            return

        self.controller._players_clocks[current_player_id] = max(
            0.0, current_clock - 1.0
        )

        if self.controller._players_clocks[current_player_id] <= 0.0:
            with contextlib.suppress(Exception):
                winner_id = self.controller._model.resign_current_player()
                self.show_timeout(current_player_id)
                if winner_id:
                    self.show_victory(winner_id)
                else:
                    self.show_player_resigned(current_player_id)
            self.render(self.controller._model.get_game_state())
            return

        self.update_timer(self.controller._players_clocks, current_player_id)
        self.update_dashboard(game_state)

    def _invia_comando(self, comando: str) -> None:
        if not self.controller:
            return

        is_game_over = self.controller._is_replay_available()
        sys_cmds = ["mosse", "help", "abbandona", "exit"]
        
        if is_game_over and comando not in sys_cmds:
            self.show_error("Partita terminata. Usa i controlli Replay in basso!")
            return

        try:
            self.controller._app([comando])
        except SystemExit:
            pass
        except Exception as e:
            self.show_error(str(e))
            return

        if self.controller._model.check_victory():
            winner_id = self.controller._model.get_game_state().get("winner")
            if winner_id and not getattr(self, "_victory_shown", False):
                self.show_victory(winner_id)

    # ------------------------------------------------------------------
    # GESTIONE REPLAY
    # ------------------------------------------------------------------

    def _replay_pause(self) -> None:
        """Mette in pausa il replay automatico se attivo."""
        if getattr(self, "_replay_timer", None):
            self._replay_timer.pause()
            self._replay_timer = None
            with contextlib.suppress(Exception):
                self.query_one("#btn_toggle", Button).label = "▶️"

    def _replay_auto_tick(self) -> None:
        """Avanza di un passo nel replay automatico."""
        if self._replay_step < self._replay_max:
            self._replay_step += 1
            self._render_replay_step()
        else:
            self._replay_pause()
            self.add_log_entry("\n[bold cyan]Replay completato.[/bold cyan]")

    def _render_replay_step(self) -> None:
        """Ricostruisce e renderizza un frame del replay."""
        if not self.controller:
            return
        replay_game = self.controller._build_replay_game(self._replay_step)
        self.render(replay_game.get_game_state())
        
        with contextlib.suppress(Exception):
            header = self.query_one("#root-header", Static)
            header.update(
                f"[bold cyan]REPLAY IN CORSO: "
                f"Passo {self._replay_step} di {self._replay_max}[/bold cyan]"
            )

    def on_replay_action_requested(self, event: ReplayActionRequested) -> None:
        if not self.controller or not self.controller._is_replay_available():
            self.show_error("Il replay è disponibile solo a partita terminata.")
            return

        if not self._in_replay_mode:
            self._in_replay_mode = True
            self._replay_max = len(self.controller._get_replay_moves())
            self._replay_step = 0
            self.add_log_entry("\n[bold cyan]▶ MODALITÀ REPLAY AVVIATA[/bold cyan]")
            self.add_log_entry("[italic]Clicca 'Menu' a destra per uscire.[/italic]")

        if event.action == "prev":
            self._replay_pause()
            if self._replay_step > 0:
                self._replay_step -= 1
            else:
                self.show_error("Inizio della partita raggiunto.")
            self._render_replay_step()
            
        elif event.action == "next":
            self._replay_pause()
            if self._replay_step < self._replay_max:
                self._replay_step += 1
            else:
                self.show_error("Fine della partita raggiunta.")
            self._render_replay_step()
            
        elif event.action == "toggle":
            if self._replay_timer is not None:
                self._replay_pause()
                self.add_log_entry("[italic]Replay automatico in pausa.[/italic]")
            else:
                self.add_log_entry("[italic]Replay automatico avviato.[/italic]")
                if self._replay_step >= self._replay_max:
                    self._replay_step = 0
                self._replay_timer = self.set_interval(0.8, self._replay_auto_tick)
                with contextlib.suppress(Exception):
                    self.query_one("#btn_toggle", Button).label = "⏸️"

    # ------------------------------------------------------------------

    def on_move_requested(self, event: MoveRequested) -> None:
        self._invia_comando(event.cell_id)

    def on_wall_placement_requested(self, event: WallPlacementRequested) -> None:
        comando = f"{event.anchor}{event.orientation}"
        self._invia_comando(comando)

    def on_button_pressed(self, event: Button.Pressed) -> None:  # type: ignore[override]
        bid = event.button.id
        if not self.controller:
            return

        if bid == "btn_prev":
            self.post_message(ReplayActionRequested("prev"))
        elif bid == "btn_next":
            self.post_message(ReplayActionRequested("next"))
        elif bid == "btn_toggle":
            self.post_message(ReplayActionRequested("toggle"))
        elif bid == "btn_storico":
            self._invia_comando("mosse")
        elif bid == "btn_aiuto":
            self.show_help()
        elif bid == "btn_abbandona":
            if getattr(self, "_victory_shown", False):
                # Se la partita è finita, questo tasto riapre il menu finale
                winner_id = self.controller._model.get_game_state().get("winner")
                msg = (
                    f"🏆 Il Giocatore P{winner_id} ha vinto!" 
                    if winner_id else "Partita terminata!"
                )
                self.push_screen(EndGameScreen(msg), callback=self._on_end_game_done)
            else:
                self._invia_comando("abbandona")
        elif bid == "btn_esci":
            self.exit()

    def action_replay_prev(self) -> None:
        self.post_message(ReplayActionRequested("prev"))

    def action_replay_next(self) -> None:
        self.post_message(ReplayActionRequested("next"))

    def action_replay_toggle(self) -> None:
        self.post_message(ReplayActionRequested("toggle"))

    def action_exit_app(self) -> None:
        self.exit()

    def _on_end_game_done(self, result: Any) -> None:
        if not isinstance(result, dict):
            return
        action = result.get("action")
        if action == "new_game":
            self._in_replay_mode = False
            self._replay_pause()
            self.push_screen(
                PlayerSelectionScreen(), callback=self._on_player_selection_done
            )
        elif action == "replay":
            if not self._in_replay_mode:
                self._in_replay_mode = True
                self._replay_max = len(self.controller._get_replay_moves())
                self._replay_step = 0
                self.add_log_entry("\n[bold cyan]▶ MODALITÀ REPLAY AVVIATA[/bold cyan]")
                self._render_replay_step()
        elif action == "quit":
            self.exit()

    def render(self, game_state: dict[str, Any]) -> None:
        self.update_board(game_state)
        self.update_dashboard(game_state)
        self.update_timer(
            getattr(self.controller, "_players_clocks", None),
            game_state.get("current_player_id"),
        )

    def update_dashboard(self, game_state: dict[str, Any] | None = None) -> None:
        if game_state is None and self.controller:
            game_state = self.controller._model.get_game_state()
        if not game_state:
            return

        players = game_state.get("players", [])
        current_player_id = game_state.get("current_player_id")
        clocks = getattr(self.controller, "_players_clocks", {})

        lines: list[str] = []
        pawns = ["🔴", "🔵", "🟢", "🟡"]

        for i, p in enumerate(players):
            if isinstance(p, dict):
                pid = p.get("_id", i + 1)
                walls = p.get("muri_rimanenti", "?")
                player_name = p.get("nome", f"P{pid}")
            else:
                try:
                    pid = getattr(p, "_id", i + 1)
                    walls = p.get_walls_count()
                    player_name = f"P{pid}"
                except Exception:
                    continue

            clock_value = clocks.get(pid)
            if clock_value is None or not getattr(
                self.controller, "_is_timed_game", False
            ):
                time_formatted = "∞"
            else:
                minutes = int(clock_value) // 60
                seconds = int(clock_value) % 60
                time_formatted = f"{minutes:02d}:{seconds:02d}"

            active_marker = "👉" if pid == current_player_id else "  "
            style = "[bold green]" if pid == current_player_id else ""
            reset = "[/bold green]" if pid == current_player_id else ""
            lines.append(
                f"{active_marker} {pawns[i]} {style}{player_name}{reset} "
                f"| Muri: {walls} | Tempo: {time_formatted}"
            )

        with contextlib.suppress(Exception):
            info = self.query_one("#players_status", Static)
            info.update("\n".join(lines))

    def update_board(self, game_state: dict[str, Any]) -> None:
        for node in self.query("GridNode"):
            if node.has_class("board-cell"):
                node.update(" ")
            node.remove_class("pawn-p1")
            node.remove_class("pawn-p2")
            node.remove_class("pawn-p3")
            node.remove_class("pawn-p4")
            node.remove_class("wall-p1")
            node.remove_class("wall-p2")
            node.remove_class("wall-p3")
            node.remove_class("wall-p4")

        players = game_state.get("players", [])
        pawns = ["🔴", "🔵", "🟢", "🟡"]
        
        for i, p in enumerate(players):
            if not p:
                continue
            
            lr, lc = None, None
            if isinstance(p, dict):
                pos = p.get("pos") or (p.get("riga"), p.get("colonna"))
                if isinstance(pos, (list, tuple)):
                    with contextlib.suppress(Exception):
                        lr, lc = int(pos[0]), int(pos[1])
            else:
                with contextlib.suppress(Exception):
                    # Conversione robusta per resistere a stringhe passate dal backend
                    px, py = p.get_position().get_coords()
                    if isinstance(px, str):
                        lc = ord(px.lower()) - ord('a')
                    else:
                        lc = int(px) - 1
                    lr = int(py) - 1

            if lr is None or lc is None:
                continue

            grid_r = lr * 2
            grid_c = lc * 2
            for node in self.query("GridNode"):
                if node.grid_r == grid_r and node.grid_c == grid_c:
                    node.update(pawns[i])
                    node.add_class(f"pawn-p{i+1}")

        walls = []
        board_obj = game_state.get("board")
        if board_obj and hasattr(board_obj, "get_walls"):
            walls = board_obj.get_walls()
        else:
            walls = game_state.get("muri") or game_state.get("walls") or []

        for muro in walls:
            with contextlib.suppress(Exception):
                if isinstance(muro, dict):
                    r = int(muro.get("riga", 0))
                    c = int(muro.get("colonna", 0))
                    oriz = bool(muro.get("orizzontale"))
                    gid = int(muro.get("giocatore_id", 0))
                else:
                    # Conversione robusta per resistere ai muri passati dal backend.
                    px, py = muro.get_start_cell().get_coords()
                    if isinstance(px, str):
                        c = ord(px.lower()) - ord('a')
                    else:
                        c = int(px) - 1
                    
                    r = int(py) - 1
                    
                    orient_str = str(muro.get_orientation()).lower()
                    oriz = (orient_str == "h")
                    gid = getattr(muro, "giocatore_id", 0)

                if r is None or c is None:
                    continue

                if oriz:
                    nodes = [
                        (r * 2 + 1, c * 2),
                        (r * 2 + 1, c * 2 + 1),
                        (r * 2 + 1, c * 2 + 2)
                    ]
                else:
                    nodes = [
                        (r * 2, c * 2 + 1),
                        (r * 2 + 1, c * 2 + 1),
                        (r * 2 + 2, c * 2 + 1)
                    ]

                for node in self.query("GridNode"):
                    if (node.grid_r, node.grid_c) in nodes:
                        node.add_class(f"wall-p{gid+1}")

    def update_timer(
        self, 
        timers: dict[int, int] | None = None, 
        current_turn: int | None = None
    ) -> None:
        with contextlib.suppress(Exception):
            if self._in_replay_mode:
                return
            header = self.query_one("#root-header", Static)
            if not timers:
                header.update("")
                return
            lines: list[str] = []
            for pid, t in timers.items():
                mark = "*" if current_turn == pid else " "
                lines.append(f"P{pid}:{int(t)}s {mark}")
            header.update(" | ".join(lines))

    def add_log_entry(self, text: str) -> None:
        with contextlib.suppress(Exception):
            log = self.query_one("#move_log", RichLog)
            log.write(text)

    def log_message(self, msg: str) -> None:
        self.add_log_entry(msg)

    def show_error(self, message: str) -> None:
        self.add_log_entry(f"[bold red]❌ Errore:[/bold red] {message}")

    def show_victory(self, player_id: int) -> None:
        with contextlib.suppress(Exception):
            if self.controller and hasattr(self.controller, "_model"):
                self.controller._model.record_event(player_id, "vittoria")

        self.add_log_entry(
            f"\n[bold green]🏆 VITTORIA:[/bold green] 🔥 "
            f"Il Giocatore P{player_id} ha vinto!"
        )
        self._set_game_over_state()
        self.push_screen(
            EndGameScreen(f"🏆 Il Giocatore P{player_id} ha vinto!"),
            callback=self._on_end_game_done,
        )

    def get_input(self) -> str:
        self.add_log_entry(
            "[italic]Input testuale non supportato. Usa l'interfaccia grafica.[/italic]"
        )
        return ""

    def show_exit(self, winner_id: int) -> None:
        self.add_log_entry(
            f"\n[bold yellow]🏳️  Abbandono:[/bold yellow] "
            f"Di conseguenza, il Giocatore P{winner_id} ha vinto!"
        )
        self._set_game_over_state()
        self.push_screen(
            EndGameScreen(f"🏳️ Abbandono! P{winner_id} vince!"),
            callback=self._on_end_game_done,
        )

    def show_exit_message(self) -> None:
        self.add_log_entry(
            "\n[bold yellow]Partita terminata. "
            "Premi 'Esci' nel pannello per chiudere il gioco.[/bold yellow]"
        )

    def show_initial_message(self) -> None:
        self.add_log_entry(
            "[bold cyan]✅ Partita Iniziata![/bold cyan]\n"
            "Muoviti o piazza muri con il mouse."
        )

    def show_help(self) -> None:
        help_text = (
            "\n[bold cyan]--- MANUALE QUORIDOR ---[/bold cyan]\n\n"
            "[bold yellow]OBIETTIVO[/bold yellow]\n"
            "Raggiungi il lato opposto della scacchiera prima del tuo "
            "avversario.\n"
            "Il giocatore 1 deve raggiungere la riga 9, il giocatore 2 "
            "la riga 1.\n"
            "In modalità 4 giocatori: P1→colonna 9, P2→colonna 1, "
            "P3→riga 9, P4→riga 1.\n\n"
            "[bold yellow]MOVIMENTO[/bold yellow]\n"
            "Muoviti di una sola cella alla volta verso qualsiasi "
            "direzione (su, giù,\nsinistra, destra). Non puoi muoverti "
            "dove c'è un altro giocatore\no attraverso un muro.\n\n"
            "[bold yellow]MURI[/bold yellow]\n"
            "In 2 giocatori: 10 muri per giocatore.\n"
            "In 4 giocatori: 5 muri per giocatore.\n"
            "I muri possono essere piazzati orizzontalmente o "
            "verticalmente e occupano due celle.\n"
            "Non puoi piazzare:\n"
            "  • Muri fuori dalla scacchiera\n"
            "  • Muri sovrapposti\n"
            "  • Muri che formano una croce\n\n"
            "[bold yellow]COORDINATE[/bold yellow]\n"
            "Le colonne sono indicate con lettere (a-i), le righe con "
            "numeri (1-9).\n\n"
            "[bold yellow]COMANDI MOUSE[/bold yellow]\n"
            "🖱️ [bold]Muovere:[/bold] Clicca sulle caselle chiare.\n"
            "🧱 [bold]Piazzare Muri:[/bold] Clicca sui solchi scuri "
            "tra le celle."
        )
        self.add_log_entry(help_text)

    def show_timeout(self, player_id: int) -> None:
        self.add_log_entry(
            f"\n[bold red]⌛ Tempo Scaduto![/bold red] "
            f"P{player_id} ha esaurito il tempo."
        )

    def prompt_new_game(self) -> str:
        return "n"

    def prompt_replay(self) -> str:
        return "n"

    def prompt_game_settings(self) -> tuple[bool, float]:
        return False, 99999.0

    def show_player_resigned(self, player_id: int) -> None:
        self.add_log_entry(
            f"\n[bold yellow]🏳️ Resa:[/bold yellow] P{player_id} si è "
            "ritirato dalla partita. Il gioco continua."
        )

    def show_move_history(self, move_history: list[dict], num_players: int) -> None:
        self.add_log_entry("\n[bold cyan]📋 --- CRONOLOGIA MOSSE ---[/bold cyan]")
        for entry in move_history:
            player_id = entry.get("player_id", "?")
            notation = entry.get("notation", "")
            move_type = entry.get("move_type", "")
            self.add_log_entry(f" P{player_id} → {move_type} {notation}")