"""Tests for the main module."""

import os
import sys

import pytest

# Add the project root directory to the Python path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

from src.main import UI  # noqa: E402


def test_ui_default_accent_color():
    """Test che il colore di accento predefinito sia 'red'."""
    ui = UI()
    assert ui.get_accent_color() == "red"


def test_ui_set_valid_accent_color():
    """Test dell'impostazione di un colore di accento valido."""
    ui = UI()
    ui.set_accent_color("blue")
    assert ui.get_accent_color() == "blue"

    # Test un altro colore valido
    ui.set_accent_color("bright_green")
    assert ui.get_accent_color() == "bright_green"


def test_ui_set_invalid_accent_color():
    """Test che l'impostazione di un colore non valido sollevi ValueError."""
    ui = UI()
    with pytest.raises(ValueError):
        ui.set_accent_color("invalid_color")

    # Il colore dell'accento deve rimanere invariato
    assert ui.get_accent_color() == "red"


def test_ui_get_accent_color():
    """Test che get_accent_color restituisca il colore corrente."""
    ui = UI()
    assert ui.get_accent_color() == "red"

    ui.set_accent_color("cyan")
    assert ui.get_accent_color() == "cyan"