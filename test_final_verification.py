#!/usr/bin/env python3
"""Final verification test for wall blocking functionality."""

from src.MODEL.Cell import Cell
from src.MODEL.Exception import MovementError
from src.MODEL.QuoridorGame import QuoridorGame


def verify_wall_blocking():
    """Verify that wall blocking works correctly in all scenarios."""
    print("\n" + "="*70)
    print("  FINAL VERIFICATION: WALL BLOCKING FUNCTIONALITY")
    print("="*70 + "\n")
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Horizontal wall blocks upward movement
    tests_total += 1
    print(f"\n[Test {tests_total}] Horizontal wall blocks upward movement")
    try:
        game = QuoridorGame()
        game._players[0].set_position(Cell(5, 5))
        game._players[1].set_position(Cell(8, 9))
        game.place_wall((5, 4, 'h'))
        game._current_turn = 1
        
        try:
            game.move_player((5, 4))
            print("  ❌ FAILED: Player jumped the wall!")
        except MovementError as e:
            if "orizzontale" in str(e).lower():
                print(f"  ✓ PASSED: {e}")
                tests_passed += 1
            else:
                print(f"  ❌ FAILED: Wrong error message: {e}")
    except Exception as e:
        print(f"  ❌ FAILED: Unexpected error: {e}")
    
    # Test 2: Horizontal wall blocks downward movement
    tests_total += 1
    print(f"\n[Test {tests_total}] Horizontal wall blocks downward movement")
    try:
        game = QuoridorGame()
        game._players[0].set_position(Cell(5, 3))
        game._players[1].set_position(Cell(8, 9))
        game.place_wall((5, 4, 'h'))
        game._current_turn = 1
        
        try:
            game.move_player((5, 4))
            print("  ❌ FAILED: Player jumped the wall!")
        except MovementError as e:
            if "orizzontale" in str(e).lower():
                print(f"  ✓ PASSED: {e}")
                tests_passed += 1
            else:
                print(f"  ❌ FAILED: Wrong error message: {e}")
    except Exception as e:
        print(f"  ❌ FAILED: Unexpected error: {e}")
    
    # Test 3: Vertical wall blocks rightward movement
    tests_total += 1
    print(f"\n[Test {tests_total}] Vertical wall blocks rightward movement")
    try:
        game = QuoridorGame()
        game._players[0].set_position(Cell(4, 5))
        game._players[1].set_position(Cell(8, 9))
        game.place_wall((5, 4, 'v'))
        game._current_turn = 1
        
        try:
            game.move_player((5, 5))
            print("  ❌ FAILED: Player jumped the wall!")
        except MovementError as e:
            if "verticale" in str(e).lower():
                print(f"  ✓ PASSED: {e}")
                tests_passed += 1
            else:
                print(f"  ❌ FAILED: Wrong error message: {e}")
    except Exception as e:
        print(f"  ❌ FAILED: Unexpected error: {e}")
    
    # Test 4: Vertical wall blocks leftward movement
    tests_total += 1
    print(f"\n[Test {tests_total}] Vertical wall blocks leftward movement")
    try:
        game = QuoridorGame()
        game._players[0].set_position(Cell(6, 5))
        game._players[1].set_position(Cell(8, 9))
        game.place_wall((5, 4, 'v'))
        game._current_turn = 1
        
        try:
            game.move_player((5, 5))
            print("  ❌ FAILED: Player jumped the wall!")
        except MovementError as e:
            if "verticale" in str(e).lower():
                print(f"  ✓ PASSED: {e}")
                tests_passed += 1
            else:
                print(f"  ❌ FAILED: Wrong error message: {e}")
    except Exception as e:
        print(f"  ❌ FAILED: Unexpected error: {e}")
    
    # Test 5: Valid moves still work around walls
    tests_total += 1
    print(f"\n[Test {tests_total}] Valid moves work around walls")
    try:
        game = QuoridorGame()
        game._players[0].set_position(Cell(5, 3))
        game._players[1].set_position(Cell(8, 9))
        game.place_wall((5, 4, 'h'))
        game._current_turn = 1
        
        # Move left should work
        try:
            game.move_player((4, 3))
            new_pos = game._players[0].get_position().get_coords()
            if new_pos == (4, 3):
                print(f"  ✓ PASSED: Valid move allowed, player at {new_pos}")
                tests_passed += 1
            else:
                print(f"  ❌ FAILED: Player at wrong position {new_pos}")
        except Exception as e:
            print(f"  ❌ FAILED: Valid move blocked: {e}")
    except Exception as e:
        print(f"  ❌ FAILED: Unexpected error: {e}")
    
    # Test 6: Error message mentions correct wall type
    tests_total += 1
    print(f"\n[Test {tests_total}] Error messages mention correct wall type")
    try:
        game = QuoridorGame()
        game._players[0].set_position(Cell(5, 4))
        game._players[1].set_position(Cell(8, 9))
        game.place_wall((5, 5, 'h'))  # Horizontal wall
        game._current_turn = 1
        
        try:
            game.move_player((5, 5))
            print("  ❌ FAILED: Player jumped the wall!")
        except MovementError as e:
            msg = str(e).lower()
            if "orizzontale" in msg and "blocca la strada" in msg:
                print(f"  ✓ PASSED: Correct message - '{e}'")
                tests_passed += 1
            else:
                print(f"  ❌ FAILED: Message format incorrect - '{e}'")
    except Exception as e:
        print(f"  ❌ FAILED: Unexpected error: {e}")
    
    # Print summary
    print("\n" + "="*70)
    print(f"  RESULTS: {tests_passed}/{tests_total} tests passed")
    print("="*70 + "\n")
    
    if tests_passed == tests_total:
        print("✓ ✓ ✓ SUCCESS! ALL TESTS PASSED! ✓ ✓ ✓")
        print("\n✓ Wall blocking is working correctly!")
        print("✓ Error messages are correct!")
        print("✓ Valid moves still work!")
        return True
    else:
        print(f"❌ FAILED: {tests_total - tests_passed} test(s) failed")
        return False


if __name__ == "__main__":
    import sys
    success = verify_wall_blocking()
    sys.exit(0 if success else 1)
