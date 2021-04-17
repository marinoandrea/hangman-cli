'''
This file contains all basic IO tests for the game Hangman.
This will test whether the basic messages are correctly formatted
and whether the Player can input data correctly.
'''
from contextlib import contextmanager
from functools import partial
from io import StringIO
from typing import Any, Callable, List

import pytest as pt
from hangman.constants import ANIMATIONS, MAX_LIVES
from hangman.core import Configurations, Guess, State, Difficulty
from hangman.io import (display, get_guess, get_play_new_game, parse_args,
                        print_error, print_info)


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
        # expecting ValueError
        assert False
    except Exception as e:
        assert isinstance(e, ValueError)
        _check_error(capsys, err)


def check_prompt(
    capsys: pt.CaptureFixture,
    monkeypatch: pt.MonkeyPatch,
    prompt_fun: Callable[[], Any],
    prompt_msg: str,
    expected_err: str,
    wrong_value: str,
    legal_value: str,
) -> Any:
    monkeypatch.setattr('sys.stdin', StringIO(f"{wrong_value}\n{legal_value}"))
    res = prompt_fun()
    captured = capsys.readouterr()
    assert captured.out == (
        f"{prompt_msg}\033[31merror: {expected_err}\033[0m\n{prompt_msg}"
    )
    return res


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


def test_parse_args_difficulty_easy(capsys: pt.CaptureFixture):
    """
    Tests for the lives argument in the parser.
    """
    res: Configurations
    res = parse_args(["-d", "easy"])
    assert res.difficulty == Difficulty.EASY


def test_parse_args_difficulty_medium(capsys: pt.CaptureFixture):
    """
    Tests for the lives argument in the parser.
    """
    res: Configurations
    res = parse_args(["-d", "medium"])
    assert res.difficulty == Difficulty.MEDIUM


def test_parse_args_difficulty_hard(capsys: pt.CaptureFixture):
    """
    Tests for the lives argument in the parser.
    """
    res: Configurations
    res = parse_args(["-d", "hard"])
    assert res.difficulty == Difficulty.HARD


def test_parse_args_difficulty_invalid():
    with pt.raises(ValueError):
        parse_args(["-d", "not_valid"])

    with pt.raises(ValueError):
        parse_args(["-d"])


def test_get_guess(monkeypatch: pt.MonkeyPatch, capsys: pt.CaptureFixture):
    """
    Basic IO test. This tests whether the get_guess functions returns
    a guess that could potentially be valid.
    """
    # assuming the initial dummy target word is "penguin"
    state = State(target_word="penguin", current_lives=1,
                  guesses=[], current_guess=None)

    # single character guess
    monkeypatch.setattr('sys.stdin', StringIO("c"))
    res: Guess = get_guess(state)
    assert "c" == res.guess and not res.whole_word

    # word of the same length guess
    monkeypatch.setattr("sys.stdin", StringIO("opossum"))
    res = get_guess(state)
    assert "opossum" == res.guess and res.whole_word
    capsys.readouterr()  # empty stdout

    # while the word has a different length the user is reprompted to guess
    check_prompt(
        capsys,
        monkeypatch,
        partial(get_guess, state),
        "Please enter your guess: ",
        "the word to be guessed has a different length",
        "pengui",
        "penguix"
    )

    # test for ASCII range
    check_prompt(
        capsys,
        monkeypatch,
        partial(get_guess, state),
        "Please enter your guess: ",
        "the character must be a valid ASCII (65-90 or 97-122)",
        "┴",
        "a"
    )


def test_initial_display(capsys: pt.CaptureFixture):
    """
    Tests the display function at the start of a game
    (when no guess is made.)
    """
    state = State(target_word="penguin", current_lives=10, guesses=[],
                  current_guess=None)
    display(state)
    captured = capsys.readouterr()
    expected_output = ["Word: _ _ _ _ _ _ _", ANIMATIONS[0], ""]
    assert captured.out == "\n".join(expected_output)


def test_dead_display(capsys: pt.CaptureFixture):
    """
    Tests the display function at the end of a game
    (when no more guesses can be made.)
    """
    state = State(target_word="penguin", current_lives=0, guesses=[],
                  current_guess=Guess("X"))
    display(state)
    captured = capsys.readouterr()
    expected_output = ["Word: _ _ _ _ _ _ _", "Guess: X", ANIMATIONS[MAX_LIVES], ""]
    assert captured.out == "\n".join(expected_output)


def test_get_play_new_game(
    monkeypatch: pt.MonkeyPatch, capsys: pt.CaptureFixture
):
    """
    Basic IO test. This tests whether the get_play_new_game function returns
    a boolean answer based on a correct [y/n] input.
    """
    res = check_prompt(
        capsys,
        monkeypatch,
        get_play_new_game,
        "Do you want to start a new game? [y/n] ",
        "you must answer yes (y) or no (n)",
        "a",
        "y",
    )
    assert res

    monkeypatch.setattr('sys.stdin', StringIO("n"))
    res = get_play_new_game()
    assert not res
