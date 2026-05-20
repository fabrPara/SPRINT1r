#!/usr/bin/env python3
"""Final interactive test - play the actual game."""

from src.CONTROLLER.GameController import GameController
from src.MODEL.QuoridorGame import QuoridorGame
from src.VIEW.CLIView import CLIView


def main():
    """Start the game with instructions."""
    print("\n" + "="*70)
    print("  QUORIDOR - TEST FINALE BLOCCO MURI")
    print("="*70)
    print("\nIstruzioni per il test:")
    print("1. P1 will place a horizontal wall at e4 (enter: e4h)")
    print("2. P2 will make a dummy move (enter: f9)")
    print("3. P1 will move towards wall from below (enter: e3)")
    print("4. P2 will move dummy (enter: e9)")
    print("5. P1 will try to move through wall (enter: e4)")
    print("   -> EXPECTED: 'Un muro orizzontale blocca la strada'")
    print("\n" + "="*70 + "\n")
    
    # Initialize game
    model = QuoridorGame()
    view = CLIView()
    controller = GameController(model, view)
    
    # Show initial board
    view.show_initial_message()
    view.render(model.get_game_state())
    
    # Game loop (simplified)
    turn = 0
    max_turns = 10
    
    while not model.check_victory() and turn < max_turns:
        try:
            user_input = input("\nEnter command (or 'quit' to exit): ").strip()
            if user_input.lower() == 'quit':
                print("Exiting...")
                break
            if not user_input:
                continue
            
            try:
                # Parse command
                import shlex
                args = shlex.split(user_input)
                controller._app(args)
            except SystemExit:
                pass  # Typer raises SystemExit
            
            turn += 1
            
        except KeyboardInterrupt:
            print("\n\nGame interrupted by user.")
            break
    
    print("\n" + "="*70)
    print("Test complete!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
