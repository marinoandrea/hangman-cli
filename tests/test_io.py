'''
This file contains all basic IO tests for the game Hangman.
This will test whether the basic messages are correctly formatted
and whether the Player can input data correctly.
'''
import pytest as pt
from hangman import print_error, print_info, parse_args, Configurations
from typing import List, Tuple


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

def test_parse_args_length(capsys: pt.CaptureFixture):
    """
    Tests whether the arugment parser behaves correctly when length is inputted.
    """
    MIN: int = 0
    MAX: int = 1
    l_tests: List[Tuple[str, str]] = [("4", "7"), ("2", "500"), ("6", "4"), ("0", "2")]

    # individual length tests in-range
    argList: List[str] = ["-m", l_tests[0][MIN]]
    res: Configurations
    res = parse_args(argList)
    assert res.min_length == int(l_tests[0][MIN])

    argList = ["-M", l_tests[0][MAX]]
    res = parse_args(argList)
    assert res.max_length == int(l_tests[0][MAX])

    argList: List[str] = ["--minimum-length", l_tests[0][MIN]]
    res: Configurations
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
    argList = ["-m", l_tests[2][MIN], "-M", l_tests[2][MAX]]
    parse_args(argList)
    captured = capsys.readouterr()
    assert captured.out == "\033[31merror: minimum length value higher than maximum length value\033[0m\n"

    # missing value
    argList = ["-m"]
    parse_args(argList)
    captured = capsys.readouterr()
    assert captured.out == "\033[31merror: missing value\033[0m\n"

    # too low values
    argList = ["-m", l_tests[3][MIN], "-M", l_tests[2][MAX]]
    parse_args(argList)
    captured = capsys.readouterr()
    assert captured.out == "\033[31merror: minimum length value too low\033[0m\n"


def test_parse_args_lives(capsys: pt.CaptureFixture):
    """
    Tests for the lives argument in the parser.
    """
    res: Configurations
    for i in range(11, -1, -1):
        res = parse_args(["-l", str(i)])
        if i > 10:
            captured = capsys.readouterr()
            assert captured.out == "\033[31merror: that many lives make the game too easy\033[0m\n"
            continue
        if i < 1:
            captured = capsys.readouterr()
            assert captured.out == "\033[31merror: having less than 1 live is not advised\033[0m\n"
            continue
        assert res.lives == i
    res = parse_args(["--lives", "5"])
    assert res.lives == 5

    