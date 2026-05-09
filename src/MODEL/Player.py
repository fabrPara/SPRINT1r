from Cell import Cell


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

def get_position(self) -> 'Cell':
    """Restituisce la cella attualmente occupata dal giocatore.

    Returns:
        Cell: La posizione attuale.
    """
    return self._position

def set_position(self, new_pos: 'Cell'):
    """Aggiorna la posizione del giocatore sulla board.

    Args:
        new_pos (Cell): La nuova cella in cui spostare il giocatore.
    """
    if not isinstance(new_pos, Cell):
        raise MovementError("La nuova posizione deve essere una Cell valida")

    self._position = new_pos