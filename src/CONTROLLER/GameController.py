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
        """Traduce stringhe tipo 'E3' o 'E3H' in indici numerici e orientamento."""
        # Regex: Lettera (A-I), Numero (1-9), Orientamento opzionale (H/V)
        match = re.match(r"^([A-I])([1-9])([HV])?$", coords_str.upper())

        if not match:
            msg = f"Input '{coords_str}' non valido. Usa il formato [A-I][1-9][H/V]"
            raise InvalidCommandError(msg)

        # CORREZIONE LOGICA:
        # group(1) è la lettera -> Colonna
        # group(2) è il numero -> Riga
        col = self._COL_MAP[match.group(1)] + 1
        row = int(match.group(2)) - 1
        orientation = match.group(3)

        return col, row, orientation

    def _setup_commands(self) -> None:
        """Configura i comandi dell'applicazione Typer."""

        @self._app.callback(invoke_without_command=True)
        def process_turn(
            mossa: str = typer.Argument(
                ..., help="Inserisci la mossa (es. 'e3' per muovere, 'e3h' per muro)."
            ),
        ):
            try:
                # 1. Traduciamo la stringa in dati logici
                col, row, orient = self._parse_coords(mossa)

                # 2. Smistiamo la logica al Modello
                if orient:
                    dati_muro = (col, row+1, orient.lower())
                    self._model.place_wall(dati_muro)
                else:
                    self._model.move_player((col, row))

                # 3. Se la mossa è valida, ricarichiamo la UI
                self._render_game()

            except Exception as e:
                self._handle_error(e)

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
                # Trasformiamo la stringa in una lista di argomenti per Typer
                args = shlex.split(user_input)
                self._app(args)
            except SystemExit:
                # Typer chiude il processo dopo ogni comando, noi lo impediamo
                if self._model.check_victory():
                    break
                continue
