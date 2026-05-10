"""Punto di ingresso principale per l'applicazione Quoridor."""

from rich import print

from src.CONTROLLER.GameController import GameController
from src.MODEL.QuoridorGame import QuoridorGame
from src.VIEW.CLIView import CLIView


def main() -> None:
    """Configura le componenti MVC e avvia il loop principale."""
    # Inizializzazione del Modello (Logica di gioco)
    model = QuoridorGame()

    # Inizializzazione della Vista (Interfaccia CLI)
    view = CLIView()

    # Inizializzazione del Controller (Coordinatore)
    controller = GameController(model, view)

    # Avvio della partita
    try:
        controller.start_game()
    except KeyboardInterrupt:
        print("\nPartita interrotta dall'utente. Alla prossima!")


if __name__ == "__main__":
    main()
