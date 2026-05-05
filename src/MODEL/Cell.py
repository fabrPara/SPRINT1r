class Cell:
    """Rappresenta una singola casella sulla scacchiera di Quoridor.

    La cella è l'unità fondamentale della board ed è definita dalle sue 
    coordinate cartesiane (x, y). Viene utilizzata per tracciare la 
    posizione dei giocatori e come punto di ancoraggio per i muri. 
    """

    def __init__(self, x: int, y: int):
        """Inizializza una nuova cella con le coordinate specificate.""" 
        """ Args:
            x (int): La coordinata orizzontale della cella.
            y (int): La coordinata verticale della cella."""
        self.x = x
        self.y = y

    def get_coords(self) -> tuple:
        """Restituisce le coordinate della cella sotto forma di tupla."""
        """Returns:
            tuple: Una tupla contenente (x, y)."""
    
        return (self.x, self.y)

    def __repr__(self):
        """Restituisce una rappresentazione leggibile della cella ."""
        return f"Cell(x={self.x}, y={self.y})"

    def __eq__(self, other):
        """Verifica se due celle sono uguali confrontando le loro coordinate."""
        if not isinstance(other, Cell):
            return False
        return self.x == other.x and self.y == other.y