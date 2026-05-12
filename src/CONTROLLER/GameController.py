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
        match = re.match(r"^([A-I])([1-9])([HV])?$", coords_str.upper())
        if not match:
            msg = f"Formato '{coords_str}' errato. Usa [A-I][1-9] (es. B2 o B2H)"
            raise InvalidCommandError(msg)

        col = self._COL_MAP[match.group(1)] + 1
        row = int(match.group(2))
        orient = match.group(3).upper() if match.group(3) else None
        return col, row, orient

    def _setup_commands(self) -> None:
        """Configura i comandi con logica match-case."""

        @self._app.callback(invoke_without_command=True)
        def process_command(
            ctx: typer.Context,
            comando: str = typer.Argument(..., help="Comando da eseguire"),
            argomento: str = typer.Argument(None, help="Coordinate (es. b2h)"),
        ):
            if ctx.resilient_parsing:
                return

            try:
                match comando.lower():
                    case "wall":
                        if not argomento:
                            raise InvalidCommandError("Uso: wall [A-I][1-9][H/V]")
                        col, row, orient = self._parse_coords(argomento)
                        if not orient:
                            raise InvalidCommandError("Manca orientamento (H/V)")
                        self._model.place_wall((col, row, orient.lower()))

                    case "move":
                        if not argomento:
                            raise InvalidCommandError("Uso: move [A-I][1-9]")
                        col, row, _ = self._parse_coords(argomento)
                        self._model.move_player((col, row))

                    case _:
                        # Solleva InvalidCommandError se il comando è ignoto
                        raise InvalidCommandError(
                            f"Comando '{comando}' non riconosciuto. "
                            "Digita 'help' per la lista comandi."
                        )

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

    def start_game(self) -> None:
        """Ciclo principale di gioco interattivo."""
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
