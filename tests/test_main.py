"""Tests for the main module."""

import os
import sys

import pytest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.main import UI


def test_ui_default_accent_color():
    """Test that the default accent color is 'red'."""
    ui = UI()
    assert ui.get_accent_color() == "red"


def test_ui_set_valid_accent_color():
    """Test setting a valid accent color."""
    ui = UI()
    ui.set_accent_color("blue")
    assert ui.get_accent_color() == "blue"

    # Test another valid color
    ui.set_accent_color("bright_green")
    assert ui.get_accent_color() == "bright_green"


def test_ui_set_invalid_accent_color():
    """Test that setting an invalid accent color raises a ValueError."""
    ui = UI()
    with pytest.raises(ValueError):
        ui.set_accent_color("invalid_color")

    # The accent color should remain unchanged
    assert ui.get_accent_color() == "red"


def test_ui_get_accent_color():
    """Test that get_accent_color returns the current accent color."""
    ui = UI()
    assert ui.get_accent_color() == "red"

    ui.set_accent_color("cyan")
    assert ui.get_accent_color() == "cyan"
