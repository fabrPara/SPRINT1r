import pytest

from src.MODEL.Exception import InvalidCommandError, TurnError, WallPlacementError
from src.MODEL.QuoridorGame import QuoridorGame


def test_game_initialization():
    """CE Valida: Turno iniziale a P1 e stato pulito."""
    game = QuoridorGame(num_players=2)
    state = game.get_game_state()
    assert state["winner"] is None
    assert game._current_turn_index == 0


def test_switch_turn_rotation():
    """CE Valida: Passaggio sequenziale dei turni di gioco."""
    game = QuoridorGame(num_players=2)
    assert game._current_turn == 1
    game.switch_turn()
    assert game._current_turn == 2


def test_invalid_wall_format_syntax_error():
    """CE Non Valida: Orientamento errato passato a place_wall."""
    game = QuoridorGame(num_players=2)
    with pytest.raises(InvalidCommandError):
        game.place_wall((3, 3, "x"))


def test_action_after_game_over():
    """VL: Blocco delle azioni se la partita presenta già un vincitore."""
    game = QuoridorGame(num_players=2)
    game._winner = 1
    with pytest.raises(TurnError):
        game.place_wall((3, 3, "h"))


def test_validate_wall_cross_intersection_error():
    """VL: validate_wall rileva l'incrocio a croce perfetto tra muri H e V."""
    game = QuoridorGame(num_players=2)
    game.place_wall((4, 3, "v"))

    with pytest.raises(WallPlacementError):
        game.place_wall((3, 3, "h"))


def test_validate_wall_outside_boundary_first_row_error():
    """VL: validate_wall impedisce il posizionamento dei muri a riga 0."""
    game = QuoridorGame(num_players=2)

    with pytest.raises(WallPlacementError):
        game.place_wall((2, 0, "h"))


def test_validate_wall_vertical_first_column_error():
    """VL: validate_wall impedisce un muro verticale nella colonna 0."""
    game = QuoridorGame(num_players=2)

    with pytest.raises(WallPlacementError):
        game.place_wall((0, 3, "v"))


def test_validate_wall_horizontal_last_column_error():
    """VL: validate_wall impedisce un muro orizzontale nell'ultima colonna."""
    game = QuoridorGame(num_players=2)

    with pytest.raises(WallPlacementError):
        game.place_wall((8, 4, "h"))


def test_game_rollback_on_placement_error():
    """CE Valida: Se la validazione fallisce, il muro viene riaccreditato."""
    game = QuoridorGame(num_players=2)
    game.place_wall((3, 3, "h"))

    p = game._get_player_by_id(game._current_turn)
    initial_walls = p.get_walls_count()

    with pytest.raises(WallPlacementError):
        game.place_wall((3, 3, "h"))

    assert p.get_walls_count() == initial_walls


def test_game_reset():
    """CE Valida: Ripristino completo dei parametri di gioco."""
    game = QuoridorGame(num_players=2)
    game.switch_turn()
    game.reset()
    assert game._current_turn_index == 0
    assert len(game._board.get_walls()) == 0