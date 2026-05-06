from rich import print


class UI:
    """Defines the configuration of the game's UI."""

    def __init__(self):
        """Initialize the game's UI with default settings."""
        self._ACCENT_COLOR: str = "red"

    def set_accent_color(self, accent_color: str):
        """Set the accent color for the game's UI.

        List of valid colors supported by the Rich library:
            - `black`
            - `red`
            - `green`
            - `yellow`
            - `blue`
            - `magenta`
            - `cyan`
            - `white`
            - `bright_black`
            - `bright_red`
            - `bright_green`
            - `bright_yellow`
            - `bright_blue`
            - `bright_magenta`
            - `bright_cyan`
            - `bright_white`

        Args:
            accent_color (str): the accent color to be used in the game's UI

        Raises:
            ValueError: if the accent color is not supported by the Rich library

        """
        RICH_COLORS: set[str] = {
            "black",
            "red",
            "green",
            "yellow",
            "blue",
            "magenta",
            "cyan",
            "white",
            "bright_black",
            "bright_red",
            "bright_green",
            "bright_yellow",
            "bright_blue",
            "bright_magenta",
            "bright_cyan",
            "bright_white",
        }

        # If the user provides an accent color, then use it
        if accent_color in RICH_COLORS:
            self._ACCENT_COLOR = accent_color
        else:
            raise ValueError(
                f"Invalid accent color '{accent_color}'. "
                "Please choose a color supported by the Rich library!"
            )

    def get_accent_color(self) -> str:
        """Get the accent color for the game's UI.

        Returns:
            accent color

        """
        return self._ACCENT_COLOR


def main():
    """Run the Quoridor game and activate the GH workflows."""
    ui = UI()
    ui.set_accent_color("blue")

    name = input("Benvenuto! Inserisci il tuo nome: ")
    print(
        f"Ciao [bold {ui.get_accent_color()}]{name}[/bold {ui.get_accent_color()}]! "
        "Iniziamo a giocare!"
    )


if __name__ == "__main__":
    main()
