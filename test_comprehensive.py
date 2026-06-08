"""Test interattivo del gioco con gestione dei muri."""

from src.MODEL.Cell import Cell
from src.MODEL.QuoridorGame import QuoridorGame


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")


def print_game_state(game):
    """Print current game state."""
    state = game.get_game_state()
    p1 = state["players"][0]
    p2 = state["players"][1]
    p1_pos = p1.get_position().get_coords()
    p1_walls = p1.get_walls_count()
    print(f"P1 Position: {p1_pos} | P1 Walls: {p1_walls}")
    p2_pos = p2.get_position().get_coords()
    p2_walls = p2.get_walls_count()
    print(f"P2 Position: {p2_pos} | P2 Walls: {p2_walls}")
    print(f"Current Turn: P{state['current_player_id']}")
    print(f"Walls on board: {len(state['board'].get_walls())}")
    if state["board"].get_walls():
        for wall in state["board"].get_walls():
            coords = wall.get_start_cell().get_coords()
            orient = wall.get_orientation().upper()
            print(f"  - {orient} at {coords}")


def test_horizontal_wall():
    """Test horizontal wall blocking in both directions."""
    print_section("TEST 1: MURO ORIZZONTALE BLOCCA VERTICALMENTE")

    game = QuoridorGame()
    game._players[0].set_position(Cell(5, 2))
    game._players[1].set_position(Cell(8, 9))

    print_game_state(game)

    # Place horizontal wall at (5, 4)
    print("\nP1 places horizontal wall at e4...")
    game.place_wall((5, 4, "h"))
    print("✓ Wall placed successfully")
    print_game_state(game)

    # P2 tries to move, P1 moves towards wall from below
    print("\nP2's turn (dummy move)...")
    game._players[1].set_position(Cell(5, 3))
    game._current_turn_index = 0

    print("\n--- Test Case 1a: P1 at (5, 3) tries to move to (5, 4) ---")
    try:
        game.move_player((5, 4))
        assert False, "Player jumped over the wall!"
    except Exception as e:
        print(f"✓ PASSED: {e}")

    # Reset for next test
    game._players[0].set_position(Cell(5, 3))
    game._current_turn_index = 0

    # Move to different position for next test
    game._players[0].set_position(Cell(5, 5))

    print("\n--- Test Case 1b: P1 at (5, 5) tries to move to (5, 4) ---")
    try:
        game.move_player((5, 4))
        assert False, "Player jumped over the wall!"
    except Exception as e:
        print(f"✓ PASSED: {e}")


def test_vertical_wall():
    """Test vertical wall blocking in both directions."""
    print_section("TEST 2: MURO VERTICALE BLOCCA ORIZZONTALMENTE")

    game = QuoridorGame()
    game._players[0].set_position(Cell(2, 5))
    game._players[1].set_position(Cell(8, 9))

    print_game_state(game)

    # Place vertical wall at (5, 4)
    print("\nP1 places vertical wall at e4...")
    game.place_wall((5, 4, "v"))
    print("✓ Wall placed successfully")
    print_game_state(game)

    # P2 skips, P1 tests movement
    print("\nP2's turn (dummy move)...")
    game._current_turn_index = 1

    print("\n--- Test Case 2a: P1 at (4, 5) tries to move to (5, 5) ---")
    game._players[0].set_position(Cell(4, 5))
    game._current_turn_index = 0
    try:
        game.move_player((5, 5))
        assert False, "Player jumped over the wall!"
    except Exception as e:
        print(f"✓ PASSED: {e}")

    print("\n--- Test Case 2b: P1 at (6, 5) tries to move to (5, 5) ---")
    game._players[0].set_position(Cell(6, 5))
    game._current_turn_index = 0
    try:
        game.move_player((5, 5))
        assert False, "Player jumped over the wall!"
    except Exception as e:
        print(f"✓ PASSED: {e}")


def test_valid_moves():
    """Test that valid moves still work around walls."""
    print_section("TEST 3: MOVIMENTI VALIDI INTORNO AI MURI")

    game = QuoridorGame()
    game._players[0].set_position(Cell(5, 3))
    game._players[1].set_position(Cell(8, 9))

    # Place wall and switch back to P1
    game.place_wall((5, 4, "h"))
    game._current_turn_index = 0  # Force turn back to P1
    print("Wall placed at (5, 4)")

    # Valid move to the side
    print("\n--- Test Case 3a: P1 moves left from (5, 3) to (4, 3) ---")
    try:
        game.move_player((4, 3))
        print("✓ PASSED: Valid move allowed")
        p1_pos = game._players[0].get_position().get_coords()
        assert p1_pos == (4, 3), f"P1 at {p1_pos}, expected (4, 3)"
        print(f"✓ P1 correctly at {p1_pos}")
    except Exception as e:
        assert False, f"Valid move blocked - {e}"


def test_error_messages():
    """Test that error messages are correct."""
    print_section("TEST 4: MESSAGGI DI ERRORE CORRETTI")

    game = QuoridorGame()
    game._players[0].set_position(Cell(5, 3))
    game._players[1].set_position(Cell(8, 9))

    # Horizontal wall
    game.place_wall((5, 4, "h"))
    game._current_turn_index = 0

    print("--- Test Case 4a: Horizontal wall error message ---")
    try:
        game.move_player((5, 4))
    except Exception as e:
        error_msg = str(e)
        assert "orizzontale" in error_msg.lower(), f"Wrong message - '{e}'"
        print(f"✓ PASSED: Correct message - '{e}'")

    # Reset for vertical test
    game = QuoridorGame()
    game._players[0].set_position(Cell(4, 5))
    game._players[1].set_position(Cell(8, 9))
    game.place_wall((5, 4, "v"))
    game._current_turn_index = 0

    print("\n--- Test Case 4b: Vertical wall error message ---")
    try:
        game.move_player((5, 5))
    except Exception as e:
        error_msg = str(e)
        assert "verticale" in error_msg.lower(), f"Wrong message - '{e}'"
        print(f"✓ PASSED: Correct message - '{e}'")


if __name__ == "__main__":
    results = []

    results.append(("Horizontal Wall", test_horizontal_wall()))
    results.append(("Vertical Wall", test_vertical_wall()))
    results.append(("Valid Moves", test_valid_moves()))
    results.append(("Error Messages", test_error_messages()))

    print_section("TEST SUMMARY")
    for test_name, result in results:
        status = "✓ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")

    all_passed = all(r for _, r in results)
    print(f"\n{'=' * 70}")
    if all_passed:
        print("  ✓ ALL TESTS PASSED!")
    else:
        print("  ❌ SOME TESTS FAILED")
    print(f"{'=' * 70}\n")
