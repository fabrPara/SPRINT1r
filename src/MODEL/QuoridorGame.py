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
        """Muove il giocatore corrente nella cella specificata dalle coordinate."""
        if len(coords) != 2:
            raise MovementError("Formato coordinate non valido. Usa una tupla (x, y).")

        target_x, target_y = coords

        if not isinstance(target_x, int) or not isinstance(target_y, int):
            raise MovementError("Coordinate non valide. Usa numeri interi.")

        # --- CONTROLLO 1: Confini della scacchiera ---
        if not (1 <= target_x <= 9 and 1 <= target_y <= 9):
            raise MovementError("Movimento fuori dai confini della scacchiera (1-9).")

        current_player = self._players[self._current_turn - 1]
        current_pos = current_player.get_position()
        curr_x, curr_y = current_pos.get_coords()

        dx = target_x - curr_x
        dy = target_y - curr_y

        opponent = self._players[1] if self._current_turn == 1 else self._players[0]
        opp_x, opp_y = opponent.get_position().get_coords()
        opp_dx = opp_x - curr_x
        opp_dy = opp_y - curr_y
        opponent_adjacent = abs(opp_dx) + abs(opp_dy) == 1

        def is_within_bounds(x: int, y: int) -> bool:
            return 1 <= x <= 9 and 1 <= y <= 9

        def is_cell_occupied(x: int, y: int) -> bool:
            return any(
                player.get_position().get_coords() == (x, y)
                for player in self._players
            )

        def segment_blocked(x1: int, y1: int, x2: int, y2: int) -> bool:
            move_dx = x2 - x1
            move_dy = y2 - y1
            for wall in self._board.get_walls():
                wx, wy = wall.get_start_cell().get_coords()
                w_orient = wall.get_orientation().lower()
                if (
                    move_dx == 0
                    and abs(move_dy) == 1
                    and w_orient == "h"
                    and wy == max(y1, y2)
                    and (wx == x1 or wx == x1 - 1)
                ):
                    return True
                if (
                    move_dy == 0
                    and abs(move_dx) == 1
                    and w_orient == "v"
                    and wx == max(x1, x2)
                    and (wy == y1 or wy == y1 + 1)
                ):
                    return True
            return False

        direct_jump_x = curr_x + 2 * opp_dx
        direct_jump_y = curr_y + 2 * opp_dy
        direct_target = (direct_jump_x, direct_jump_y)
        diagonal_targets = []
        pivot_blocked = segment_blocked(curr_x, curr_y, opp_x, opp_y)

        if opponent_adjacent:
            if (target_x, target_y) == (opp_x, opp_y):
                raise MovementError("Movimento non valido: cella occupata.")

            if (target_x, target_y) == direct_target:
                if (
                    pivot_blocked
                    or not is_within_bounds(direct_jump_x, direct_jump_y)
                    or is_cell_occupied(direct_jump_x, direct_jump_y)
                    or segment_blocked(opp_x, opp_y, direct_jump_x, direct_jump_y)
                ):
                    raise MovementError(
                        "Salto non permesso: muro blocca il passaggio."
                    )
                current_player.set_position(Cell(direct_jump_x, direct_jump_y))
                self.switch_turn()
                return

            if opp_dx == 0:
                diagonal_targets = [
                    (opp_x - 1, opp_y),
                    (opp_x + 1, opp_y),
                ]
            else:
                diagonal_targets = [
                    (opp_x, opp_y - 1),
                    (opp_x, opp_y + 1),
                ]

            if pivot_blocked and (target_x, target_y) in diagonal_targets:
                raise MovementError(
                    "Salto non permesso: muro blocca il passaggio."
                )

            if (target_x, target_y) in diagonal_targets:
                direct_blocked = (
                    not is_within_bounds(direct_jump_x, direct_jump_y)
                    or is_cell_occupied(direct_jump_x, direct_jump_y)
                    or segment_blocked(opp_x, opp_y, direct_jump_x, direct_jump_y)
                )
                if not direct_blocked:
                    raise MovementError(
                        "Movimento non valido: puoi muoverti solo di una cella."
                    )
                if is_cell_occupied(target_x, target_y):
                    raise MovementError("Movimento non valido: cella occupata.")
                if segment_blocked(opp_x, opp_y, target_x, target_y):
                    raise MovementError(
                        "Salto non permesso: muro blocca il passaggio."
                    )
                current_player.set_position(Cell(target_x, target_y))
                self.switch_turn()
                return

        if not ((abs(dx) == 1 and dy == 0) or (dx == 0 and abs(dy) == 1)):
            raise MovementError(
                "Movimento non valido: puoi muoverti solo di una cella."
            )

        # --- CONTROLLO 3: Presenza di muri basato sul vostro sistema ---
        for wall in self._board.get_walls():
            wx, wy = wall.get_start_cell().get_coords()
            w_orient = wall.get_orientation().lower()

            # Movimento Verticale (dy != 0)
            # Un muro H in (wx, wy) blocca il passaggio tra y e y-1
            # se la colonna è wx o wx+1.
            if (
                dy != 0
                and w_orient == "h"
                and wy == max(curr_y, target_y)
                and (wx == curr_x or wx == curr_x - 1)
            ):
                raise MovementError("Un muro orizzontale blocca il passaggio.")

            # Movimento Orizzontale (dx != 0)
            # Un muro V in (wx, wy) blocca il passaggio tra x e x-1
            # se la riga è wy o wy-1.
            if (
                dx != 0
                and w_orient == "v"
                and wx == max(curr_x, target_x)
                and (wy == curr_y or wy == curr_y + 1)
            ):
                raise MovementError("Un muro verticale blocca il passaggio.")

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
        """Controlla se uno dei giocatori ha raggiunto la vittoria."""
        for player in self._players:
            current_pos = player.get_position().get_coords()
            current_row = current_pos[1]

            if current_row == player._target_row:
                self._winner = player._id
                return True

        return False

    def resign_current_player(self) -> int:
        """Riconosce la resa del giocatore di turno e restituisce il vincitore."""
        if self._winner is not None:
            return self._winner

        self._winner = 2 if self._current_turn == 1 else 1
        return self._winner

    def reset(self) -> None:
        """Resetta il gioco per una nuova partita."""
        self._board = Board()

        p1_start = Cell(5, 1)
        p2_start = Cell(5, 9)

        p1 = Player(player_id=1, start_pos=p1_start, target_row=9)
        p2 = Player(player_id=2, start_pos=p2_start, target_row=1)

        self._players = [p1, p2]
        self._current_turn = 1
        self._winner = None
    
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
            self._board.add_wall(new_wall,self._players)
        except Exception as e:
            current_player._walls_count += 1
            raise e

        self.switch_turn()
