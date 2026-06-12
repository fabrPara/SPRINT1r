"""Punto di ingresso principale per l'applicazione Quoridor."""

import sys

from rich import print

from src.CONTROLLER.GameController import GameController
from src.MODEL.QuoridorGame import QuoridorGame
from src.VIEW.AdvancedView import AdvancedView  # Importa la nuova GUI


def main() -> None:
    """Configura le componenti MVC e avvia il loop principale."""
    # Inizializzazione del Modello (Logica di gioco)
    model = QuoridorGame()

    # Controlliamo se l'utente ha passato l'argomento "gui" da terminale
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        view = AdvancedView()
        controller = GameController(model, view)
        
        # COLLEGAMENTO CRITICO: Diamo alla vista il riferimento del controller
        view.controller = controller
        
        # Facciamo partire l'interfaccia grafica di Textual
        view.run()
    else:
        # Altrimenti, se non specifichi "gui", parte la vecchia CLI di prima
        from src.VIEW.CLIView import CLIView
        view = CLIView()
        controller = GameController(model, view)
        try:
            controller.start_game()
        except KeyboardInterrupt:
            print("\nPartita interrotta dall'utente. Alla prossima!")


if __name__ == "__main__":
    main()