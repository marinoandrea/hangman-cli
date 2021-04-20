'''
This file contains all basic IO tests for the game Hangman.
This will test whether the basic messages are correctly formatted
and whether the Player can input data correctly.
'''
from functools import partial
from io import StringIO
from typing import Any, Callable

import pytest as pt
from hangman.constants import ANIMATIONS, MAX_LIVES
from hangman.core import Difficulty, Guess, State
from hangman.io import (display, get_guess, get_play_new_game, parse_args,
                        print_error, print_info)


def check_error(capsys: pt.CaptureFixture, expected: str):
    captured = capsys.readouterr()
    assert captured.out == f"\033[31merror: {expected}\033[0m\n"


def check_info(capsys: pt.CaptureFixture, info: str):
    captured = capsys.readouterr()
    assert captured.out == f"\033[96minfo: {info}\033[0m\n"


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
    check_error(capsys, "test")


def test_print_info(capsys: pt.CaptureFixture):
    """
    Tests whether the passed string to print_info is
    actually formatted to be blue.
    """
    print_info("congratulations, you have won this game!")
    check_info(capsys, "congratulations, you have won this game!")


def test_parse_args_length(capsys: pt.CaptureFixture):
    """
    Tests whether the arugment parser behaves correctly when
    length is inputted.
    """
    # individual length tests in-range
    args = ["-m", "4"]
    res = parse_args(args)
    assert res.min_length == 4

    args = ["-M", "7"]
    res = parse_args(args)
    assert res.max_length == 7

    args = ["--minimum-length", "4"]
    res = parse_args(args)
    assert res.min_length == 4

    args = ["--maximum-length", "7"]
    res = parse_args(args)
    assert res.max_length == 7

    # # both minimum and maximum test
    args = ["-m", "4", "-M", "7"]
    res = parse_args(args)
    assert res.min_length == 4
    assert res.max_length == 7

    args = ["-M", "500", "-m", "2"]
    res = parse_args(args)
    assert res.min_length == 2
    assert res.max_length == 500

    args = [
        "--maximum-length", "500",
        "--minimum-length", "2"
    ]
    res = parse_args(args)
    assert res.min_length == 2
    assert res.max_length == 500

    # min higher than max
    with pt.raises(ValueError):
        args = ["-m", "6", "-M", "4"]
        parse_args(args)
        check_error("minimum length value higher than maximum length value")

    # too low values
    with pt.raises(ValueError):
        args = ["-m", "0"]
        parse_args(args)
        check_error("minimum length value too low")

    with pt.raises(ValueError):
        args = ["-M", "2"]
        parse_args(args)
        check_error("maximum length value too low")

    # value higher than longest word
    with pt.raises(ValueError):
        args = ["-m", "999", "-M", "1000"]
        parse_args(args)
        check_error("The are no words as long as 999 in the game.")


def test_parse_args_lives(capsys: pt.CaptureFixture):
    """
    Tests for the lives argument in the parser.
    """
    for i in range(11, -1, -1):
        try:
            res = parse_args(["-l", str(i)])
            # an exception should be thrown here
            if i > 10 or i < 1:
                assert False
        except Exception as e:
            if i > 10:
                check_error(capsys, "that many lives make the game too easy")
                assert isinstance(e, ValueError)
                continue
            if i < 1:
                check_error(capsys, "having less than 1 live is not advised")
                assert isinstance(e, ValueError)
                continue
        assert res.lives == i
    res = parse_args(["--lives", "5"])
    assert res.lives == 5


def test_parse_args_difficulty(capsys: pt.CaptureFixture):
    """
    Tests for the lives argument in the parser.
    """
    res = parse_args(["-d", "easy"])
    assert res.difficulty == Difficulty.EASY

    res = parse_args(["-d", "medium"])
    assert res.difficulty == Difficulty.MEDIUM

    res = parse_args(["-d", "hard"])
    assert res.difficulty == Difficulty.HARD

    with pt.raises(ValueError):
        parse_args(["-d", "not_valid"])


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

    # test for zero length input
    check_prompt(
        capsys,
        monkeypatch,
        partial(get_guess, state),
        "Please enter your guess: ",
        "you must guess a character or the entire word",
        "",
        "a"
    )

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
    (when no more guesses can be made) when the player
    has lost.
    """
    state = State(
        target_word="penguin",
        current_lives=0,
        guesses=[],
        current_guess=Guess("X"),
        is_running=False,
        is_victory=False
    )
    display(state)
    captured = capsys.readouterr()
    expected_output = [
        "\nSorry, you have lost! 😢\n",
        "Word: p e n g u i n",
        "Guess: X",
        ANIMATIONS[MAX_LIVES],
        ""
    ]
    assert captured.out == "\n".join(expected_output)


def test_win_display(capsys: pt.CaptureFixture):
    """
    Tests the display function at the end of a game
    (when no more guesses can be made) when the player
    has won.
    """
    state = State(
        target_word="penguin",
        current_lives=1,
        guesses=[],
        current_guess=Guess(guess="penguin", whole_word=True),
        is_running=False,
        is_victory=True
    )
    display(state)
    captured = capsys.readouterr()
    expected_output = [
        "\nCongratulations, you have guessed the word! 🥳\n",
        "Word: p e n g u i n",
        "Guess: penguin",
        ANIMATIONS[MAX_LIVES - 1],
        ""
    ]
    assert captured.out == "\n".join(expected_output)


def test_bad_state_display(capsys: pt.CaptureFixture):
    """
    Tests the display function when an illegal state is
    passed as an argument.
    """
    state = State(
        target_word="penguin",
        current_lives=-1,
        guesses=[],
        current_guess=Guess(guess="penguin", whole_word=True),
        is_running=False,
        is_victory=True
    )
    with pt.raises(RuntimeError):
        display(state)


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
