"""Simulazione interattiva del gioco con test del blocco dei muri."""

from src.MODEL.Cell import Cell
from src.MODEL.QuoridorGame import QuoridorGame
from src.VIEW.CLIView import CLIView


def simulate_game():
    """Simulate a game session with wall blocking tests."""
    print("\n" + "=" * 70)
    print("  SIMULAZIONE GIOCO QUORIDOR - TEST BLOCCO MURI")
    print("=" * 70 + "\n")

    # Create game and manually set up scenario
    model = QuoridorGame()
    view = CLIView()

    # Manual setup:
    # P1 at e2, P2 at e8
    model._players[0].set_position(Cell(5, 2))
    model._players[1].set_position(Cell(5, 8))
    model._current_turn = 1

    print("Initial Setup:")
    print("  P1 at e2 (5, 2)")
    print("  P2 at e8 (5, 8)")
    print("\n--- Rendering initial board ---")
    view.render(model.get_game_state())

    # P1's turn: place horizontal wall at e4-f4
    print("\n--- P1's Action: Place horizontal wall at e4 (e4h) ---")
    try:
        model.place_wall((5, 4, "h"))
        print("✓ Wall placed successfully")
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    view.render(model.get_game_state())

    # P2 moves (dummy move to right)
    print("\n--- P2's Action: Move to f8 ---")
    try:
        model.move_player((6, 8))
        print("✓ Move successful")
    except Exception as e:
        print(f"Error: {e}")

    view.render(model.get_game_state())

    # P1 tries to move DOWN towards wall
    print("\n--- P1's Action: Try to move down from e2 to e3 ---")
    try:
        model.move_player((5, 3))
        print("✓ Move successful")
        print(f"  P1 now at {model._players[0].get_position().get_coords()}")
    except Exception as e:
        print(f"❌ Blocked: {e}")

    view.render(model.get_game_state())

    # P2 dummy move
    model._current_turn = 2
    model._players[1].set_position(Cell(6, 8))
    model._current_turn = 1

    # P1 tries to move UP through wall (this should fail now!)
    print("\n--- P1's Action: Try to move up from e3 to e4 (BLOCKED BY WALL!) ---")
    try:
        model.move_player((5, 4))
        print("❌ ERROR: PLAYER JUMPED OVER THE WALL!")
        return False
    except Exception as e:
        print(f"✓ CORRECTLY BLOCKED: {e}")
        return True


def test_wall_blocking_from_other_side():
    """Test wall blocking from the other side."""
    print("\n" + "=" * 70)
    print("  TEST: WALL BLOCKING FROM THE OTHER SIDE")
    print("=" * 70 + "\n")

    model = QuoridorGame()
    view = CLIView()

    # Setup: P1 at e5, P2 at f9
    model._players[0].set_position(Cell(5, 5))
    model._players[1].set_position(Cell(6, 9))
    model._current_turn = 1

    print("Initial Setup:")
    print("  P1 at e5 (5, 5)")
    print("  P2 at f9 (6, 9)")

    # P1 places wall
    print("\n--- P1 places wall at e4 ---")
    model.place_wall((5, 4, "h"))
    print("✓ Wall placed")

    view.render(model.get_game_state())

    # P2 dummy move
    model._current_turn = 2

    # P1 tries to move up through wall (from below)
    print("\n--- P1 at (5,5) tries to move UP through wall at e4 ---")
    model._current_turn = 1
    try:
        model.move_player((5, 4))
        print("❌ ERROR: PLAYER JUMPED OVER THE WALL!")
        return False
    except Exception as e:
        print(f"✓ CORRECTLY BLOCKED: {e}")
        return True


if __name__ == "__main__":
    result1 = simulate_game()
    result2 = test_wall_blocking_from_other_side()

    print("\n" + "=" * 70)
    print("  RESULTS")
    print("=" * 70)
    if result1 and result2:
        print("✓ ALL SIMULATION TESTS PASSED!")
        print("✓ Walls correctly block player movement!")
    else:
        print("❌ Some tests failed")
    print("=" * 70 + "\n")
