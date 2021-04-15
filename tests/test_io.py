'''
This file contains all basic IO tests for the game Hangman.
This will test whether the basic messages are correctly formatted
and whether the Player can input data correctly.
'''
from contextlib import contextmanager
from io import StringIO
from typing import List

import pytest as pt
from hangman.core import Configurations, State
from hangman.io import (get_guess, get_play_new_game, parse_args, print_error,
                        print_info)


def _check_error(capsys: pt.CaptureFixture, expected: str):
    captured = capsys.readouterr()
    assert captured.out == f"\033[31merror: {expected}\033[0m\n"


def _check_info(capsys: pt.CaptureFixture, info: str):
    captured = capsys.readouterr()
    assert captured.out == f"\033[96minfo: {info}\033[0m\n"


@contextmanager
def check_value_error(capsys: pt.CaptureFixture, err: str):
    try:
        yield
    except Exception as e:
        assert isinstance(e, ValueError)
        _check_error(capsys, err)


def test_print_error(capsys: pt.CaptureFixture):
    """
    Tests whether the passed string to print_error is
    actually formatted to be red.
    """
    print_error("test")
    _check_error(capsys, "test")


def test_print_info(capsys: pt.CaptureFixture):
    """
    Tests whether the passed string to print_info is
    actually formatted to be blue.
    """
    print_info("congratulations, you have won this game!")
    _check_info(capsys, "congratulations, you have won this game!")


def test_parse_args_length(capsys: pt.CaptureFixture):
    """
    Tests whether the arugment parser behaves correctly when
    length is inputted.
    """
    MIN = 0
    MAX = 1
    l_tests = [("4", "7"), ("2", "500"), ("6", "4"), ("0", "2")]

    # individual length tests in-range
    argList: List[str] = ["-m", l_tests[0][MIN]]
    res = parse_args(argList)
    assert res.min_length == int(l_tests[0][MIN])

    argList = ["-M", l_tests[0][MAX]]
    res = parse_args(argList)
    assert res.max_length == int(l_tests[0][MAX])

    argList = ["--minimum-length", l_tests[0][MIN]]
    res = parse_args(argList)
    assert res.min_length == int(l_tests[0][MIN])

    argList = ["--maximum-length", l_tests[0][MAX]]
    res = parse_args(argList)
    assert res.max_length == int(l_tests[0][MAX])

    # # both minimum and maximum test
    argList = ["-m", l_tests[0][MIN], "-M", l_tests[0][MAX]]
    res = parse_args(argList)
    assert res.min_length == int(l_tests[0][MIN])
    assert res.max_length == int(l_tests[0][MAX])

    argList = ["-M", l_tests[1][MAX], "-m", l_tests[1][MIN]]
    res = parse_args(argList)
    assert res.min_length == int(l_tests[1][MIN])
    assert res.max_length == int(l_tests[1][MAX])

    argList = ["--maximum-length", l_tests[1][MAX], "--minimum-length", l_tests[1][MIN]]
    res = parse_args(argList)
    assert res.min_length == int(l_tests[1][MIN])
    assert res.max_length == int(l_tests[1][MAX])

    ### error tests ###

    # min higher than max
    with check_value_error(capsys, "minimum length value higher than maximum length value"):
        argList = ["-m", l_tests[2][MIN], "-M", l_tests[2][MAX]]
        parse_args(argList)

    # missing value
    with check_value_error(capsys, "missing_value"):
        argList = ["-m"]
        parse_args(argList)

    # too low values
    with check_value_error(capsys, "minimum length value too low"):
        argList = ["-m", l_tests[3][MIN], "-M", l_tests[2][MAX]]
        parse_args(argList)


def test_parse_args_lives(capsys: pt.CaptureFixture):
    """
    Tests for the lives argument in the parser.
    """
    res: Configurations
    for i in range(11, -1, -1):
        try:
            res = parse_args(["-l", str(i)])
            # an exception should be thrown here
            if i > 10 or i < 1:
                assert False
        except Exception as e:
            if i > 10:
                _check_error(capsys, "that many lives make the game too easy")
                assert isinstance(e, ValueError)
                continue
            if i < 1:
                _check_error(capsys, "having less than 1 live is not advised")
                assert isinstance(e, ValueError)
                continue
        assert res.lives == i
    res = parse_args(["--lives", "5"])
    assert res.lives == 5


def test_get_guess(monkeypatch: pt.MonkeyPatch, capsys: pt.CaptureFixture):
    """
    Basic IO test. This tests whether the get_guess functions returns
    a guess that could potentially be valid.
    """
    # assuming the initial dummy target word is "penguin"
    state = State(target_word="penguin", current_lives=1, guesses=[])

    # single character guess
    monkeypatch.setattr('sys.stdin', StringIO("c"))
    res = get_guess(state)
    assert "c" == res.guess

    # word of the same length guess
    monkeypatch.setattr("sys.stdin", StringIO("opossum"))
    res = get_guess(state)
    assert "opossum" == res.guess

    captured = capsys.readouterr()  # empty stdout

    # while the word has a different length the user is reprompted to guess
    monkeypatch.setattr("sys.stdin", StringIO('pengui\npenguix'))
    res = get_guess(state)

    captured = capsys.readouterr()
    expected = "the word to be guessed has a different length"
    assert captured.out == (
        f"Please enter your guess: \033[31merror: {expected}\033[0m\n"
        + "Please enter your guess: "
    )


def test_get_play_new_game(
    monkeypatch: pt.MonkeyPatch, capsys: pt.CaptureFixture
):
    """
    Basic IO test. This tests whether the get_play_new_game function returns
    a boolean answer based on a correct [y/n] input.
    """
    monkeypatch.setattr('sys.stdin', StringIO("a\ny"))
    res = get_play_new_game()

    captured = capsys.readouterr()
    assert captured.out == (
        "Do you want to start a new game? [y/n] " +
        "\033[31merror: you must answer yes (y) or no (n)\033[0m\n" +
        "Do you want to start a new game? [y/n] "
    )
    assert res

    monkeypatch.setattr('sys.stdin', StringIO("n"))
    res = get_play_new_game()
    assert not res
