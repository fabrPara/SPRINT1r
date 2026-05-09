from .Cell import Cell
from .Exception import WallDepletionError


class Player:
    """Rappresenta un giocatore all'interno del gioco Quoridor.

    Gestisce lo stato del giocatore, inclusa la sua posizione attuale sulla
    board, il numero di muri rimanenti e l'obiettivo di vittoria (riga target).
    """

    def __init__(self, player_id: int, start_pos: "Cell", target_row: int):
        """Inizializza un nuovo giocatore.

        Args:
            player_id(int): Identificativo univoco del giocatore.
            start_pos(Cell): Istanza di Cell che rappresenta la posizione iniziale.
            target_row(int): La coordinata Y che il giocatore deve raggiungere per vincere.

        """  # noqa: E501
        self._id = player_id
        self._position = start_pos
        self._walls_count = 10  # Numero standard di muri in Quoridor
        self._target_row = target_row

    """ ritorna il numero di muri rimanenti del giocatore. """

    def get_walls_count(self) -> int:
        return self._walls_count

    def use_wall(self) -> None:
        """Scala un muro dalla riserva del giocatore."""
        if self._walls_count <= 0:
            raise WallDepletionError("Non hai più muri a disposizione!")
        self._walls_count -= 1
