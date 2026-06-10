"""Modulo per la gestione della scacchiera di gioco."""

from .Cell import Cell
from .Exception import WallPlacementError
from .Wall import Wall


class Board:
    """Rappresenta la scacchiera di gioco.

    Questa classe gestisce gli elementi strutturali della scacchiera,
    mantenendo traccia delle celle che lo compongono e dei muri
    posizionati al suo interno.
    """

    def __init__(self):
        """Inizializza una nuova istanza della scacchiera (Board).

        Crea le strutture dati iniziali (liste vuote) necessarie per
        memorizzare le celle e i muri. Gli attributi sono definiti
        come protetti (prefisso '_') per indicare che il loro accesso
        e la loro modifica dovrebbero avvenire tramite futuri metodi
        della classe.

        Attributes:
            _cells (list[Cell]): Una lista destinata a contenere gli
                oggetti di tipo `Cell` (le caselle).
            _walls (list[Wall]): Una lista destinata a contenere gli
                oggetti di tipo `Wall` (i muri o ostacoli).

        """
        self._cells: list[Cell] = []
        self._walls: list[Wall] = []

    def get_walls(self):
        """Ritorna la lista dei muri attualmente posizionati sulla board."""
        return self._walls

    def add_wall(self, wall: Wall) -> None:
        """Valida e aggiunge un muro alla scacchiera.

        Args:
            wall (Wall): Il muro orizzontale da aggiungere.

        Raises:
            WallPlacementError: Se il posizionamento viola le regole.

        """
        self._validate_wall(wall)
        self._walls.append(wall)

    def _validate_wall(self, new_wall: Wall) -> None:
        """Controlla le collisioni e i confini fisici per tutti i muri.

        Args:
            new_wall (Wall): L'oggetto Wall da validare.

        """
        nx = new_wall.get_start_cell().x
        ny = new_wall.get_start_cell().y
        orientation = new_wall.get_orientation().lower()

        # 1. Controllo confini della scacchiera
        if orientation == "h":
            if nx < 1 or nx > 8 or ny < 2 or ny > 9:
                if nx == 9 or ny == 1:
                    msg = (
                        "Il muro che si vuole posizionare "
                        "esce parzialmente dalla scacchiera"
                    )
                    raise WallPlacementError(msg)
                raise WallPlacementError("Il muro esce dai confini della scacchiera.")
        elif orientation == "v":
            if nx < 1 or nx > 9 or ny < 2 or ny > 8:
                raise WallPlacementError("Il muro esce dai confini della scacchiera.")
        else:
            raise WallPlacementError("Orientamento muro non valido.")

        # 2. Controllo sovrapposizioni con muri esistenti
        for w in self._walls:
            wx = w.get_start_cell().x
            wy = w.get_start_cell().y
            w_orientation = w.get_orientation().lower()

            # Sovrapposizione esatta
            if nx == wx and ny == wy and orientation == w_orientation:
                raise WallPlacementError(
                    "C'è già un muro esattamente in questa posizione."
                )

            # Sovrapposizione parziale (stesso orientamento)
            if orientation == w_orientation:
                if orientation == "h" and ny == wy and abs(nx - wx) == 1:
                    raise WallPlacementError(
                        "Il muro si sovrappone parzialmente a un muro "
                        "orizzontale esistente"
                    )
                if orientation == "v" and nx == wx and abs(ny - wy) == 1:
                    raise WallPlacementError(
                        "Il muro si sovrappone parzialamente a un muro "
                        "verticale esistente"
                    )

            # Incrocio tra muri di orientamenti diversi
            if orientation != w_orientation and nx == wx and ny == wy:
                raise WallPlacementError("I muri non possono incrociarsi.")

