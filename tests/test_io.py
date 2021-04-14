import pytest
from hangman import *
import sys

# This file contains all basic IO tests for the game Hangman.
# This will test whether the basic messages are correctly formatted and whether the Player can input
# data correctly.

# Tests whether the passed string to print_error is actually formatted to be red.
def test_print_error(capsys):
    print_error("test")
    captured = capsys.readouterr()
    assert captured.out == f"\033[31mtest\033[0m\n"

# Tests whether the passed string to print_info is actually formatted to be blue
def test_print_info(capsys):
    print_info("congratulations, you have won this game!")
    captured = capsys.readouterr()
    assert captured.out == f"\033[96mcongratulations, you have won this game!\033[0m\n"

