import pytest

from src.MODEL.Cell import Cell
from src.MODEL.Exception import WallDepletionError
from src.MODEL.Player import Player


def test_player_initialization():
    """CE Valida: Controllo dei valori alla nascita del player."""
    start_cell = Cell(4, 0)
    player = Player(player_id=1, start_pos=start_cell, target_row=8)
    assert player._id == 1
    assert player.get_position() == start_cell
    assert player.get_walls_count() == 10


def test_player_set_position():
    """CE Valida: Modifica della posizione della pedina."""
    player = Player(player_id=1, start_pos=Cell(4, 0), target_row=8)
    new_cell = Cell(4, 1)
    player.set_position(new_cell)
    assert player.get_position() == new_cell


def test_player_use_wall_decrement():
    """CE Valida: Consumo regolare di un muro dalla riserva."""
    player = Player(player_id=1, start_pos=Cell(4, 0), target_row=8)
    player.use_wall()
    assert player.get_walls_count() == 9


def test_player_wall_depletion_error():
    """VL: Tentativo di usare un muro quando la riserva è vuota (0)."""
    player = Player(
        player_id=1, start_pos=Cell(4, 0), target_row=8, walls_count=0
    )
    with pytest.raises(WallDepletionError):
        player.use_wall()