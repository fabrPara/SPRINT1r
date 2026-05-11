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
        """Valida e aggiunge un muro alla plancia.

        Args:
            wall (Wall): Il muro orizzontale da aggiungere.

        Raises:
            WallPlacementError: Se il posizionamento viola le regole.

        """
        self._validate_wall(wall)
        self._walls.append(wall)

    def _validate_wall(self, new_wall: Wall) -> None:
        """Controlla le collisioni e i confini fisici (solo orizzontali).

        Args:
            new_wall (Wall): L'oggetto Wall da validare.

        """
        nx = new_wall._start_cell.x
        ny = new_wall._start_cell.y

       
        if nx < 2 or nx > 8 or ny < 2 or ny > 9:
            raise WallPlacementError("Il muro esce dai confini della plancia.")
        
       
        # 2. Controllo sovrapposizioni con muri esistenti (Issue 3: solo orizzontali)
        for w in self._walls:
            wx = w._start_cell.x
            wy = w._start_cell.y

            # Sovrapposizione esatta (partono dalle stesse identiche coordinate)
            if nx == wx and ny == wy:
                raise WallPlacementError(
                    "C'è già un muro esattamente in questa posizione."
                )

            # Sovrapposizione parziale (si toccano sulla stessa linea orizzontale)
            if ny == wy and abs(nx - wx) == 1:
                raise WallPlacementError(
                    "Il muro si sovrappone parzialmente a un muro orizzontale esistente"
                )


# TODO DA AGGIUNGERE CONTROLLO "IF NO 'V' " E CONTROLLO SUI MURI A CROCE - ISSUE 4!!!!
