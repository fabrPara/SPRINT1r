from .Cell import Cell


class Wall:
    """Questa classe rappresenta un muro all'interno del gioco "Quoridor".

    Scopo e responsabilità della classe: Memorizzare la posizione iniziale del muro e il
    suo orientamento (che può essere orizzontale oppure verticale).

    """

    def __init__(self, start_cell: "Cell", orientation: str):
        """Inizializza un nuovo muro.

        Args:
            start_cell (Cell): _description_
            orientation (str): _description_

        """
        self._start_cell = start_cell
        self._orientation = orientation

    def get_start_cell(self) -> Cell:
        """Restituisce la cella di partenza del muro."""
        return self._start_cell

    def get_orientation(self) -> str:
        """Restituisce l'orientamento del muro."""
        return self._orientation
