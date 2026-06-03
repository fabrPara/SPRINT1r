"""Modulo controller principale del gioco Quoridor."""

import re
import shlex
import threading
import time

import typer

from src.MODEL.Exception import (
    InvalidCommandError,
    MovementError,
    TurnError,
    WallDepletionError,
    WallPlacementError,
)
from src.MODEL.QuoridorGame import QuoridorGame
from src.VIEW.BaseView import BaseView


class GameController:
    """Gestisce l'input dell'utente e coordina il flusso tra Modello e Vista."""

    def __init__(self, model: QuoridorGame, view: BaseView) -> None:
        """Inizializza il controller con le istanze di modello e vista."""
        self._model = model
        self._view = view
        self._exit_requested = False
        self._COL_MAP = {char: i for i, char in enumerate("ABCDEFGHI")}

        self._is_timed_game = False
        self._default_time_seconds = 180.0

        self._players_clocks: dict[int, float] = {
            1: self._default_time_seconds,
            2: self._default_time_seconds,
        }

        self._turn_data: dict[str, object] = {
            "input_utente": None,
            "tempo_scaduto": False,
        }

        self._app = typer.Typer(
            add_completion=False,
            help="Gestione comandi Quoridor.",
        )
        self._setup_commands()

    # ------------------------------------------------------------------
    # Setup / Reset
    # ------------------------------------------------------------------

    def _init_clocks(self, player_ids: list[int]) -> None:
        """Inizializza i clock per tutti i giocatori attivi."""
        self._players_clocks = {pid: self._default_time_seconds for pid in player_ids}

    def _reset_game(self) -> None:
        """Resetta il gioco e richiede i nuovi settaggi dal menu."""
        num_players = self._ask_num_players()
        self._model.reset(num_players=num_players)

        usa_tempo, secondi = self._view.prompt_game_settings()
        self._is_timed_game = usa_tempo
        self._default_time_seconds = secondi if usa_tempo else 99999.0

        player_ids = [p._id for p in self._model.get_game_state()["players"]]
        self._init_clocks(player_ids)

    def _ask_num_players(self) -> int:
        """Chiede il numero di giocatori se la view lo supporta, altrimenti default 2."""  # noqa: E501
        if hasattr(self._view, "prompt_num_players"):
            return self._view.prompt_num_players()  # pyright: ignore[reportAttributeAccessIssue]
        return 2

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------

    def _parse_coords(self, coords_str: str) -> tuple[int, int, str | None]:
        """Traduce coordinate tipo 'E3' o 'E3H' in indici numerici."""
        match = re.match(r"^([A-Ia-i])([1-9])([HVhv])?$", coords_str)
        if not match:
            msg = f"Formato '{coords_str}' errato. Usa [A-I][1-9] (es. b2 o b2h)"
            raise InvalidCommandError(msg)

        col = self._COL_MAP[match.group(1).upper()] + 1
        row = int(match.group(2))
        orient = match.group(3).lower() if match.group(3) else None
        return col, row, orient

    # ------------------------------------------------------------------
    # Comandi Typer
    # ------------------------------------------------------------------

    def _setup_commands(self) -> None:
        """Configura i comandi dell'applicazione Typer."""

        @self._app.callback(invoke_without_command=True)
        def process_command(
            ctx: typer.Context,
            comando: str = typer.Argument(..., help="Comando da eseguire"),
        ) -> None:
            if ctx.resilient_parsing:
                return

            try:
                comando_lower = comando.lower()

                match comando_lower:
                    case "abbandona":
                        self._handle_resign()
                        return

                    case "exit":
                        self._view.show_exit_message()
                        self._exit_requested = True
                        return

                    case "help":
                        self._view.show_help()
                        self._render_game()
                        return

                    case "mosse":
                        self._show_move_history()
                        return

                    case _:
                        col, row, orient = self._parse_coords(comando)
                        if orient:
                            self._model.place_wall((col, row, orient))
                        else:
                            self._model.move_player((col, row))

                self._render_game()

            except Exception as e:
                self._handle_error(e)

    def _handle_resign(self) -> None:
        """Gestisce il comando 'abbandona' per entrambe le modalità."""
        state = self._model.get_game_state()
        num_players: int = state.get("num_players", 2)
        resigning_id: int = state["current_player_id"]

        result = self._model.resign_current_player()

        if num_players == 4 and result == 0:
            # Partita 4P: giocatore rimosso, gli altri continuano
            self._view.show_player_resigned(resigning_id)
            self._render_game()
        else:
            # Partita 2P o ultimo giocatore rimasto in 4P → vittoria
            self._view.show_exit(result)
            response = self._view.prompt_new_game()
            if response == "s":
                self._reset_game()
                self._render_game()
            else:
                self._view.show_exit_message()
                self._exit_requested = True

    def _show_move_history(self) -> None:
        """Mostra la cronologia delle mosse effettuate nella partita."""
        state = self._model.get_game_state()
        move_history = self._model.get_move_history()
        num_players = state.get("num_players", 2)
        
        self._view.show_move_history(move_history, num_players)
        self._render_game()

    # ------------------------------------------------------------------
    # Errori e rendering
    # ------------------------------------------------------------------

    def _handle_error(self, e: Exception) -> None:
        """Gestisce e visualizza gli errori catturati durante il gioco."""
        valid_errors = (
            MovementError,
            WallPlacementError,
            WallDepletionError,
            InvalidCommandError,
            TurnError,
        )
        if isinstance(e, valid_errors):
            self._view.show_error(str(e))
        else:
            self._view.show_error(f"Errore inatteso: {e}")

    def _render_game(self) -> None:
        """Richiede alla vista di renderizzare lo stato attuale del gioco."""
        state = self._model.get_game_state()

        if self._is_timed_game:
            state["clocks"] = self._players_clocks
        else:
            state["clocks"] = {
                pid: 99999.0 for pid in [p._id for p in state["players"]]
            }

        self._view.render(state)

    # ------------------------------------------------------------------
    # Threading (input + timer)
    # ------------------------------------------------------------------

    def _get_input_worker(self) -> None:
        """Thread Worker dedicato alla cattura bloccante dell'input."""
        comando = self._view.get_input()
        if not self._turn_data["tempo_scaduto"]:
            self._turn_data["input_utente"] = comando

    def _timer_worker(self, tempo_disponibile: float) -> None:
        """Thread Worker che monitora lo scorrere del tempo residuo."""
        ora_inizio = time.time()
        while (time.time() - ora_inizio) < tempo_disponibile:
            if self._turn_data["input_utente"] is not None or self._exit_requested:
                return
            time.sleep(0.05)
        self._turn_data["tempo_scaduto"] = True

    # ------------------------------------------------------------------
    # Loop principale
    # ------------------------------------------------------------------

    def start_game(self) -> None:
        """Ciclo principale di gioco interattivo con supporto multi-threading."""
        # Selezione numero giocatori
        num_players = self._ask_num_players()
        self._model.reset(num_players=num_players)

        # Configurazione tempo
        usa_tempo, secondi = self._view.prompt_game_settings()
        self._is_timed_game = usa_tempo
        if usa_tempo:
            self._default_time_seconds = secondi

        player_ids = [p._id for p in self._model.get_game_state()["players"]]
        self._init_clocks(player_ids)

        self._view.show_initial_message()
        self._render_game()

        while not self._exit_requested:
            while not self._model.check_victory() and not self._exit_requested:
                curr_id = self._model.get_game_state()["current_player_id"]

                self._turn_data["input_utente"] = None
                self._turn_data["tempo_scaduto"] = False

                if self._is_timed_game:
                    tempo_residuo = self._players_clocks.get(curr_id, 0.0)
                    ora_inizio_turno = time.time()

                    t_input = threading.Thread(
                        target=self._get_input_worker, daemon=True
                    )
                    t_timer = threading.Thread(
                        target=self._timer_worker,
                        args=(tempo_residuo,),
                        daemon=True,
                    )

                    t_input.start()
                    t_timer.start()

                    while (
                        self._turn_data["input_utente"] is None
                        and not self._turn_data["tempo_scaduto"]
                    ):
                        time.sleep(0.05)

                    durata_mossa = time.time() - ora_inizio_turno

                    if self._turn_data["tempo_scaduto"]:
                        self._players_clocks[curr_id] = 0.0
                        self._view.show_timeout(curr_id)
                        self._model.resign_current_player()
                        break

                    nuovo_tempo = self._players_clocks[curr_id] - durata_mossa
                    self._players_clocks[curr_id] = max(0.0, nuovo_tempo)

                    user_input = self._turn_data["input_utente"]
                else:
                    user_input = self._view.get_input()

                if not user_input or self._exit_requested:
                    continue

                args = shlex.split(str(user_input))
                if not args:
                    continue

                if args[0].lower() in {"wall", "move"}:
                    self._view.show_error(
                        "Hai sbagliato comando. Usa solo coordinate come "
                        f"'e3h' o 'e3' senza il prefisso '{args[0].lower()}'."
                    )
                    continue

                try:
                    self._app(args)
                except SystemExit:
                    if self._model.check_victory():
                        break
                    continue

            if self._exit_requested:
                break

            game_state = self._model.get_game_state()
            winner_id = game_state["winner"]

            if winner_id or self._model.check_victory():
                self._view.show_victory(winner_id)

                response = self._view.prompt_new_game()
                if response == "s":
                    self._reset_game()
                    self._render_game()
                else:
                    self._view.show_exit_message()
                    self._exit_requested = True
