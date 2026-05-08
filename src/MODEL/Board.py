"""Modulo per la gestione del tabellone di gioco."""

from .Cell import Cell
from .Exception import WallPlacementError
from .Wall import Wall


class Board:
    """Rappresenta il tabellone di gioco.

    Questa classe gestisce gli elementi strutturali del tabellone,
    mantenendo traccia delle celle che lo compongono e dei muri
    posizionati al suo interno.
    """

    def __init__(self):
        """Inizializza una nuova istanza del tabellone (Board).

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
        self._cells: list[Cell] = []  # noqa: F821
        self._walls: list[Wall] = []  # noqa: F821


    def get_walls(self):
        """Ritorna la lista dei muri attualmente posizionati sulla board."""
        return self._walls
    
    def add_wall(self, wall: Wall) -> None:
        """Valida e aggiunge un muro alla plancia."""
        self._validate_wall(wall)
        self._walls.append(wall)

    def _validate_wall(self, new_wall: Wall) -> None:
        """Controlla le collisioni e i confini fisici."""
        nx = new_wall._start_cell.x
        ny = new_wall._start_cell.y
        no = new_wall._orientation

        # 1. Controllo dei limiti (la griglia dei muri va da 0 a 7)
        if nx < 0 or nx > 7 or ny < 0 or ny > 7:
            raise WallPlacementError("Il muro esce dai confini della plancia.")

        # 2. Controllo incroci e sovrapposizioni
        for w in self._walls:
            wx = w._start_cell.x
            wy = w._start_cell.y
            wo = w._orientation

            # Se partono dallo stesso punto esatto
            if nx == wx and ny == wy:
                if no == wo:
                    raise WallPlacementError("C'è già un muro esattamente in questa posizione.")  # noqa: E501
                else:
                    raise WallPlacementError("I muri non possono incrociarsi a croce.")

            # Sovrapposizione parziale (si toccano sulla stessa linea)
            if no == 'h' and wo == 'h' and ny == wy and abs(nx - wx) == 1:
                raise WallPlacementError("Il muro si sovrappone parzialmente a un muro orizzontale esistente.")  # noqa: E501
            
            if no == 'v' and wo == 'v' and nx == wx and abs(ny - wy) == 1:
                raise WallPlacementError("Il muro si sovrappone parzialmente a un muro verticale esistente.")  # noqa: E501
