from .Board import Board
from .Cell import Cell
from .Exception import InvalidCommandError, MovementError, TurnError
from .Player import Player
from .Wall import Wall


class QuoridorGame:
    """Classe principale per il gioco Quoridor.

    Gestisce la logica del tabellone, i giocatori e il loro turno.
    Fornisce metodi per muovere i giocatori, posizionare muri, verificare il vincitore.
    """

    def __init__(self):
        """Inizializza una nuova partita di Quoridor."""
        self._board = Board()

        p1_start = Cell(5, 1)
        p2_start = Cell(5, 9)

        p1 = Player(player_id=1, start_pos=p1_start, target_row=9)
        p2 = Player(player_id=2, start_pos=p2_start, target_row=1)

        self._players = [p1, p2]
        self._current_turn = 1
        self._winner = None

    def switch_turn(self):
        """Cambia il turno passando al giocatore successivo."""
        self._current_turn = 2 if self._current_turn == 1 else 1

    def move_player(self, coords: tuple[int, int]) -> None:
        """Muove il giocatore corrente nella cella specificata dalle coordinate.

        Args:
            coords (tuple[int, int]): Le coordinate della destinazione nel formato
                (x, y).

        Raises:
            MovementError: Se il movimento non è consentito.

        """
        if len(coords) != 2:
            raise MovementError("Formato coordinate non valido. Usa una tupla (x, y).")

        target_x, target_y = coords

        if not isinstance(target_x, int) or not isinstance(target_y, int):
            raise MovementError("Coordinate non valide. Usa numeri interi.")

        current_player = self._players[self._current_turn - 1]
        current_pos = current_player.get_position()
        curr_x, curr_y = current_pos.get_coords()

        dx = abs(target_x - curr_x)
        dy = abs(target_y - curr_y)

        if not ((dx == 1 and dy == 0) or (dx == 0 and dy == 1)):
            raise MovementError(
                "Movimento non valido: puoi muoverti solo di una cella in "
                "orizzontale o verticale."
            )

        current_player.set_position(Cell(target_x, target_y))
        self.switch_turn()

    def get_game_state(self) -> dict:
        """Ritorna lo stato attuale del gioco per permetterne il rendering."""
        return {
            "board": self._board,
            "players": self._players,
            "current_player_id": self._current_turn,
            "winner": self._winner,
        }

    def check_victory(self) -> bool:
        pass

    def place_wall(self, coords: tuple[int, int, str]) -> None:
        """Piazza un muro per il giocatore corrente."""
        if self._winner is not None:
            raise TurnError("La partita è già finita.")

        if len(coords) != 3 or coords[2] not in ["h", "v"]:
            raise InvalidCommandError("Orientamento non valido. Usa 'h' o 'v'.")

        current_player = self._players[self._current_turn - 1]
        current_player.use_wall()

        start_cell = Cell(coords[0], coords[1])
        new_wall = Wall(start_cell=start_cell, orientation=coords[2])

        try:
            self._board.add_wall(new_wall)
        except Exception as e:
            current_player._walls_count += 1
            raise e 

        self.switch_turn()
