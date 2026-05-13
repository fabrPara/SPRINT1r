import re
import shlex

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
    """Gestisce l'input utente e coordina Modello e Vista."""

    def __init__(self, model: QuoridorGame, view: BaseView):
        """Inizializza il controller con modello e vista."""
        self._model = model
        self._view = view
        self._exit_requested = False
        self._COL_MAP = {char: i for i, char in enumerate("ABCDEFGHI")}
        self._app = typer.Typer(add_completion=False)
        self._setup_commands()

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

    def _setup_commands(self) -> None:
        """Configura i comandi con logica match-case."""

        @self._app.callback(invoke_without_command=True)
        def process_command(
            ctx: typer.Context,
            comando: str = typer.Argument(..., help="Comando da eseguire"),
        ):
            if ctx.resilient_parsing:
                return

            try:
                comando_lower = comando.lower()

                # Comandi speciali
                match comando_lower:
                    case "abbandona":
                        winner_id = self._model.resign_current_player()
                        self._view.show_exit(winner_id)
                        response = self._view.prompt_new_game()
                        if response == "s":
                            self._reset_game()
                            self._render_game()
                        else:
                            self._view.show_exit_message()
                            self._exit_requested = True
                        return

                    case "exit":
                        self._view.show_exit_message()
                        self._exit_requested = True
                        return

                    case "help":
                        self._view.show_help()
                        self._render_game()
                        return

                    case _:
                        # Prova a parsare come coordinate
                        col, row, orient = self._parse_coords(comando)
                        if orient:
                            # Ha orientamento (H/V) -> comando di piazzamento muro
                            self._model.place_wall((col, row, orient))
                        else:
                            # Senza orientamento -> comando di movimento
                            self._model.move_player((col, row))

                self._render_game()

            except Exception as e:
                self._handle_error(e)

    def _handle_error(self, e: Exception) -> None:
        """Visualizza gli errori tramite la vista."""
        valid_errors = (
            MovementError,
            WallPlacementError,
            WallDepletionError,
            InvalidCommandError,
            TurnError,
        )
        msg = str(e) if isinstance(e, valid_errors) else f"Errore: {e}"
        self._view.show_error(msg)

    def _render_game(self) -> None:
        """Richiede il rendering dello stato attuale."""
        self._view.render(self._model.get_game_state())

    def _reset_game(self) -> None:
        """Resetta il gioco per una nuova partita."""
        self._model.reset()

    def start_game(self) -> None:
        """Ciclo principale di gioco interattivo."""
        self._view.show_initial_message()
        self._render_game()
        while not self._model.check_victory() and not self._exit_requested:
            user_input = self._view.get_input()
            if not user_input:
                continue
            try:
                args = shlex.split(user_input)
                self._app(args)
            except SystemExit:
                if self._model.check_victory():
                    break
                continue

        if self._exit_requested:
            return

        if self._model.check_victory():
            game_state = self._model.get_game_state()
            winner_id = game_state["winner"]
            self._view.show_victory(winner_id)
