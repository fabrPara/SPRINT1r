"""Modulo per la gestione del tabellone di gioco."""

from src.UTILS.PathFinder import PathFinder

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

    def add_wall(self, wall: Wall, players: list) -> None:
        """Valida e aggiunge un muro alla plancia.

        Args:
            wall (Wall): Il muro orizzontale da aggiungere.
            players (list): La lista dei giocatori.

        Raises:
            WallPlacementError: Se il posizionamento viola le regole.

        """
        self._validate_wall(wall, players)
        self._walls.append(wall)

    def _validate_wall(self, new_wall: Wall, players: list) -> None:
        """Controlla le collisioni e i confini fisici per tutti i muri.

        Args:
            new_wall (Wall): L'oggetto Wall da validare.
            players (list): La lista dei giocatori.

        """
        nx = new_wall.get_start_cell().x
        ny = new_wall.get_start_cell().y
        orientation = new_wall.get_orientation().lower()

        if orientation == "h":
            if nx < 1 or nx > 8 or ny < 2 or ny > 9:
                if nx == 9 or ny == 1:
                    msg = (
                        "Il muro che si vuole posizionare "
                        "esce parzialmente dalla scacchiera"
                    )
                    raise WallPlacementError(msg)
                raise WallPlacementError("Il muro esce dai confini della plancia.")
        elif orientation == "v":
            if nx < 2 or nx > 9 or ny < 2 or ny > 9:
                if ny == 1:
                    msg = (
                        "Il muro che si vuole posizionare "
                        "esce parzialmente dalla scacchiera"
                    )
                    raise WallPlacementError(msg)
                raise WallPlacementError("Il muro esce dai confini della plancia.")
        else:
            raise WallPlacementError("Orientamento muro non valido.")

        # 2. Controllo sovrapposizioni con muri esistenti (TUA LOGICA ORIGINALE)
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

            # Intersezione a croce perfetta (condividono lo stesso centro)
            if orientation != w_orientation and nx == wx and ny == wy:
                raise WallPlacementError("I muri non possono incrociarsi a croce.")

        simulated_walls = list(self._walls) + [new_wall]

        for p in players:
            p_coords = p.get_position().get_coords()

            # Raccoglie le coordinate di tutti gli ALTRI giocatori in gara rispetto a 'p'  # noqa: E501
            other_positions = [
                other.get_position().get_coords()
                for other in players
                if other._id != p._id
            ]

            # Esegue il controllo del percorso personalizzato per il giocatore corrente
            if not PathFinder.has_path(
                p_coords, other_positions, p._target_row, simulated_walls
            ):
                raise WallPlacementError(
                    f"Mossa illegale: interrompe l'ultimo percorso di P{p._id}."
                )
