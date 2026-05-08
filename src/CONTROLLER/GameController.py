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
    """Gestisce l'input dell'utente e coordina il flusso tra Modello e Vista."""

    def __init__(self, model: QuoridorGame, view: BaseView):
        """Inizializza il controller con le istanze di modello e vista."""
        self._model = model
        self._view = view
        self._COL_MAP = {char: i for i, char in enumerate("ABCDEFGHI")}
        self._app = typer.Typer(
            add_completion=False,
            help="Gestione comandi Quoridor.",
        )
        self._setup_commands()

    def _parse_coords(self, coords_str: str) -> tuple[int, int, str | None]:
        """Traduce stringhe tipo '3B' o '2AV' in indici numerici."""
        match = re.match(r"^([1-9])([A-I])([HV])?$", coords_str.upper())

        if not match:
            msg = f"Input '{coords_str}' non valido. Usa il formato [1-9][A-I][H/V]."
            raise InvalidCommandError(msg)

        row = int(match.group(1)) - 1
        col = self._COL_MAP[match.group(2)]
        orientation = match.group(3)

        return row, col, orientation

    def _setup_commands(self) -> None:
        """Configura i comandi dell'applicazione Typer."""

    def _handle_error(self, e: Exception) -> None:
        """Gestisce e visualizza gli errori catturati durante il gioco."""
        valid_errors = (
            MovementError,
            WallPlacementError,
            WallDepletionError,
            TurnError,
            InvalidCommandError,
        )
        if isinstance(e, valid_errors):
            self._view.show_error(str(e))
        else:
            self._view.show_error(f"Errore inatteso: {e}")

    def _render_game(self) -> None:
        """Richiede alla vista di renderizzare lo stato attuale del gioco."""
        self._view.render(self._model.get_game_state())

    def start_game(self) -> None:
        """Avvia il ciclo principale di gioco interattivo."""
        self._render_game()
        while not self._model.check_victory():
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
