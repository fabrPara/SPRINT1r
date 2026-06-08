import pytest

from src.MODEL.Board import Board
from src.MODEL.Cell import Cell
from src.MODEL.Exception import WallPlacementError
from src.MODEL.Player import Player
from src.MODEL.Wall import Wall


def test_board_initialization_empty():
    """CE Valida: Verifica che la board nasca senza muri inseriti."""
    board = Board()
    assert len(board.get_walls()) == 0


def test_board_add_wall_successful():
    """CE Valida: Inserimento riuscito di un muro in una zona libera."""
    board = Board()
    p1 = Player(1, Cell(4, 0), 8)
    p2 = Player(2, Cell(4, 8), 0)

    wall = Wall(Cell(2, 2), "h")
    board.add_wall(wall, [p1, p2])
    assert wall in board.get_walls()


def test_board_add_wall_overlap_same_orientation():
    """CE Non Valida: Sovrapposizione nello stesso punto e orientamento."""
    board = Board()
    p1 = Player(1, Cell(4, 0), 8)
    p2 = Player(2, Cell(4, 8), 0)

    wall1 = Wall(Cell(3, 3), "h")
    board.add_wall(wall1, [p1, p2])

    wall2 = Wall(Cell(3, 3), "h")
    with pytest.raises(WallPlacementError):
        board.add_wall(wall2, [p1, p2])


def test_board_add_wall_cross_intersection_h_v():
    """VL: Rilevamento dell'incrocio a croce perfetto (H su V)."""
    board = Board()
    p1 = Player(1, Cell(4, 0), 8)
    p2 = Player(2, Cell(4, 8), 0)

    wall_v = Wall(Cell(4, 3), "v")
    board.add_wall(wall_v, [p1, p2])

    wall_h = Wall(Cell(3, 3), "h")
    with pytest.raises(WallPlacementError):
        board.add_wall(wall_h, [p1, p2])


def test_board_add_wall_cross_intersection_v_h():
    """VL: Rilevamento dell'incrocio a croce perfetto (V su H)."""
    board = Board()
    p1 = Player(1, Cell(4, 0), 8)
    p2 = Player(2, Cell(4, 8), 0)

    wall_h = Wall(Cell(3, 3), "h")
    board.add_wall(wall_h, [p1, p2])

    wall_v = Wall(Cell(4, 3), "v")
    with pytest.raises(WallPlacementError):
        board.add_wall(wall_v, [p1, p2])