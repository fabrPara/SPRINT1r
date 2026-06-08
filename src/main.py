"""Punto di ingresso principale per l'applicazione Quoridor."""

from rich import print

from src.CONTROLLER.GameController import GameController
from src.MODEL.QuoridorGame import QuoridorGame
from src.VIEW.CLIView import CLIView


class UI:
    """Gestione dell'interfaccia utente e delle preferenze."""

    VALID_COLORS = {
        "red", "blue", "green", "yellow", "cyan", "magenta",
        "bright_red", "bright_blue", "bright_green", "bright_yellow",
        "bright_cyan", "bright_magenta", "black", "white"
    }

    def __init__(self) -> None:
        """Inizializza l'UI con il colore di accento predefinito."""
        self._accent_color = "red"

    def get_accent_color(self) -> str:
        """Restituisce il colore di accento corrente.

        Returns:
            str: Il colore di accento attuale.

        """
        return self._accent_color

    def set_accent_color(self, color: str) -> None:
        """Imposta il colore di accento.

        Args:
            color (str): Il colore da impostare.

        Raises:
            ValueError: Se il colore non è valido.

        """
        if color not in self.VALID_COLORS:
            raise ValueError(f"Colore non valido: {color}")
        self._accent_color = color


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
