"""Test di movimenti diagonali e movimenti complessi."""

from src.MODEL.Cell import Cell
from src.MODEL.Exception import MovementError
from src.MODEL.QuoridorGame import QuoridorGame


def test_diagonal_movement_attempt():
    """Test: tentativo di movimento diagonale (deve fallire)."""
    print("\n" + "=" * 60)
    print("TEST: MOVIMENTO DIAGONALE (deve fallire)")
    print("=" * 60)

    game = QuoridorGame()
    game._players[0].set_position(Cell(5, 1))
    game._players[1].set_position(Cell(8, 9))

    print(f"P1 posizione: {game._players[0].get_position().get_coords()}")
    print("P1 tenta movimento diagonale da (5, 1) a (6, 2)...")

    try:
        game.move_player((6, 2))
        print("❌ ERRORE: Ha permesso movimento diagonale!")
    except MovementError as e:
        print(f"✓ Corretto: {e}")


def test_multiple_walls():
    """Test: muri multipli."""
    print("\n" + "=" * 60)
    print("TEST: MURI MULTIPLI")
    print("=" * 60)

    game = QuoridorGame()
    game._players[0].set_position(Cell(5, 1))
    game._players[1].set_position(Cell(8, 9))

    # Piazza muro H in e4
    game.place_wall((5, 4, "h"))
    print("✓ Piazzato muro H in (5, 4)")

    # Piazza muro V in e3
    game._current_turn_index = 0
    game.place_wall((5, 3, "v"))
    print("✓ Piazzato muro V in (5, 3)")

    # Stampa muri
    print(f"\nMuri sulla board: {len(game._board.get_walls())}")
    for wall in game._board.get_walls():
        start = wall.get_start_cell().get_coords()
        orient = wall.get_orientation().upper()
        print(f"  - {orient} at {start}")


def test_wall_overlap_detection():
    """Test: rilevamento sovrapposizione muri."""
    print("\n" + "=" * 60)
    print("TEST: RILEVAMENTO SOVRAPPOSIZIONE MURI")
    print("=" * 60)

    game = QuoridorGame()
    game._players[0].set_position(Cell(5, 1))
    game._players[1].set_position(Cell(8, 9))

    # Piazza primo muro
    game.place_wall((5, 4, "h"))
    print("✓ Piazzato primo muro H in (5, 4)")

    # Tenta di piazzare muro sovrapposto
    game._current_turn_index = 0
    try:
        game.place_wall((5, 4, "h"))
        print("❌ ERRORE: Ha permesso sovrapposizione!")
    except Exception as e:
        print(f"✓ Bloccato: {e}")


def test_wall_blocking_from_different_directions():
    """Test: muro blocca da tutte le direzioni."""
    print("\n" + "=" * 60)
    print("TEST: MURO BLOCCA DA TUTTE LE DIREZIONI")
    print("=" * 60)

    game = QuoridorGame()

    # Piazza muro H tra righe 4 e 5, colonne 5-6
    game._players[0].set_position(Cell(5, 1))
    game._players[1].set_position(Cell(8, 9))
    game.place_wall((5, 4, "h"))
    print("✓ Piazzato muro H in (5, 4)")

    # Test 1: Da basso verso alto
    print("\nTest 1: Movimento da (5, 5) a (5, 4)")
    game._players[0].set_position(Cell(5, 5))
    game._current_turn_index = 0
    try:
        game.move_player((5, 4))
        print("❌ ERRORE: Ha saltato il muro!")
    except MovementError as e:
        print(f"✓ Bloccato: {e}")

    # Test 2: Da alto verso basso
    print("\nTest 2: Movimento da (5, 3) a (5, 4)")
    game._players[0].set_position(Cell(5, 3))
    game._current_turn_index = 0
    try:
        game.move_player((5, 4))
        print("❌ ERRORE: Ha saltato il muro!")
    except MovementError as e:
        print(f"✓ Bloccato: {e}")

    # Test 3: Colonna adiacente (colonna 6)
    print("\nTest 3: Movimento da (6, 3) a (6, 4)")
    game._players[0].set_position(Cell(6, 3))
    game._current_turn_index = 0
    try:
        game.move_player((6, 4))
        print("❌ ERRORE: Ha saltato il muro!")
    except MovementError as e:
        print(f"✓ Bloccato: {e}")


if __name__ == "__main__":
    test_diagonal_movement_attempt()
    test_multiple_walls()
    test_wall_overlap_detection()
    test_wall_blocking_from_different_directions()
