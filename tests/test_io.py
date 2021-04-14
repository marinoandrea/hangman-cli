'''
This file contains all basic IO tests for the game Hangman.
This will test whether the basic messages are correctly formatted
and whether the Player can input data correctly.
'''
import pytest as pt
from hangman import print_error, print_info


def test_print_error(capsys: pt.CaptureFixture):
    """
    Tests whether the passed string to print_error is
    actually formatted to be red.
    """
    print_error("test")
    captured = capsys.readouterr()
    assert captured.out == "\033[31mtest\033[0m\n"


def test_print_info(capsys: pt.CaptureFixture):
    """
    Tests whether the passed string to print_info is
    actually formatted to be blue.
    """
    print_info("congratulations, you have won this game!")
    captured = capsys.readouterr()
    assert captured.out == "\033[96mcongratulations, you have won this game!\033[0m\n"
