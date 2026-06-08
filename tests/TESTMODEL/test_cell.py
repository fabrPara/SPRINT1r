from src.MODEL.Cell import Cell


def test_cell_initialization_valid():
    """CE Valida: Inizializzazione corretta delle coordinate."""
    cell = Cell(4, 2)
    assert cell.x == 4
    assert cell.y == 2
    assert cell.get_coords() == (4, 2)


def test_cell_boundary_values():
    """VL: Verifica dei valori limite sui bordi della scacchiera."""
    min_cell = Cell(0, 0)
    max_cell = Cell(8, 8)
    assert min_cell.get_coords() == (0, 0)
    assert max_cell.get_coords() == (8, 8)


def test_cell_equality():
    """CE Valida e Non Valida per il confronto tra celle."""
    c1 = Cell(3, 5)
    c2 = Cell(3, 5)
    c3 = Cell(4, 5)

    assert c1 == c2
    assert c1 != c3
    assert c1 != "not_a_cell"


def test_cell_representation():
    """CE Valida: Verifica del metodo __repr__."""
    cell = Cell(1, 7)
    assert repr(cell) == "Cell(x=1, y=7)"