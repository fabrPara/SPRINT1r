from src.MODEL.Cell import Cell
from src.MODEL.Wall import Wall


def test_wall_initialization_horizontal():
    """CE Valida: Creazione di un muro orizzontale."""
    start_cell = Cell(2, 3)
    wall = Wall(start_cell, "h")
    assert wall.get_start_cell() == start_cell
    assert wall.get_orientation() == "h"


def test_wall_initialization_vertical():
    """CE Valida: Creazione di un muro verticale."""
    start_cell = Cell(5, 5)
    wall = Wall(start_cell, "v")
    assert wall.get_start_cell() == start_cell
    assert wall.get_orientation() == "v"