#!/usr/bin/env python3
"""Interactive test for wall blocking - automated scenario."""

import sys
from unittest.mock import patch

from src.CONTROLLER.GameController import GameController
from src.MODEL.Cell import Cell
from src.MODEL.QuoridorGame import QuoridorGame
from src.VIEW.CLIView import CLIView


def run_automated_test():
    """Run automated test of wall blocking."""
    print("\n" + "="*70)
    print("  TEST AUTOMATICO: BLOCCO MURI NEL GIOCO INTERATTIVO")
    print("="*70 + "\n")
    
    # Create game
    model = QuoridorGame()
    view = CLIView()
    controller = GameController(model, view)
    
    # Manually set up the scenario
    model._players[0].set_position(Cell(5, 2))
    model._players[1].set_position(Cell(5, 8))
    
    print("Scenario:")
    print("  P1 starts at e2")
    print("  P2 starts at e8")
    print("\nTest sequence:")
    print("  1. P1 places horizontal wall at e4")
    print("  2. P2 moves to f8 (dummy move)")
    print("  3. P1 moves to e3 (valid)")
    print("  4. P2 moves (dummy)")
    print("  5. P1 tries to move to e4 (MUST FAIL - blocked by wall)")
    print("\n" + "-"*70 + "\n")
    
    # Simulate commands
    commands = [
        "e4h",      # P1 places wall at e4
        "f8",       # P2 moves to f8
        "e3",       # P1 moves to e3
        "e8",       # P2 dummy move
        "e4",       # P1 tries to jump wall (should fail)
    ]
    
    for i, cmd in enumerate(commands, 1):
        print(f"\n[{i}/5] Executing command: {cmd}")
        try:
            args = [cmd]
            with patch('sys.argv', ['controller'] + args):
                controller._app(args)
            
            # Get current state
            state = model.get_game_state()
            p1_pos = state["players"][0].get_position().get_coords()
            p2_pos = state["players"][1].get_position().get_coords()
            
            print(f"     Command executed. P1: {p1_pos}, P2: {p2_pos}")
            
        except SystemExit:
            pass  # Typer raises SystemExit on success
        except Exception as e:
            print(f"     ✓ Blocked as expected: {e}")
    
    print("\n" + "-"*70)
    print("\nTest Complete!")
    
    # Verify final state
    state = model.get_game_state()
    p1_pos = state["players"][0].get_position().get_coords()
    
    print("\nFinal State:")
    print(f"  P1 Position: {p1_pos}")
    print(f"  P1 Walls Remaining: {state['players'][0].get_walls_count()}")
    print(f"  Walls on Board: {len(state['board'].get_walls())}")
    
    if p1_pos == (5, 3):
        print("\n✓ SUCCESS: Wall blocking works correctly!")
        print("✓ Player did not jump the wall!")
        return True
    else:
        print(f"\n❌ FAILED: P1 at {p1_pos}, expected (5, 3)")
        return False


if __name__ == "__main__":
    success = run_automated_test()
    sys.exit(0 if success else 1)
