from argparse import ArgumentParser
from enum import Enum, unique
from functools import wraps
from typing import Callable, List

from hangman.constants import MAX_LENGTH, MAX_LIVES, MIN_LENGTH
from hangman.core import Configurations, Guess, State


@unique
class colors(Enum):
    value: str

    RED = '\033[31m'
    END = '\033[0m'
    BLUE = '\033[96m'

    def __str__(self) -> str:
        return self.value


def print_error(string: str):
    print(f"{colors.RED}error: {string}{colors.END}")


def print_info(string: str):
    print(f"{colors.BLUE}info: {string}{colors.END}")


def parse_args(argList: List[str]) -> Configurations:
    # specifying the argument parser
    parser = ArgumentParser(description="configuration of hangman game")
    parser.add_argument(
        "-m", "--minimum-length",
        type=int,
        default=MIN_LENGTH,
        help="specifies the minimum length of the word that can be guessed")
    parser.add_argument(
        "-M", "--maximum-length",
        type=int,
        default=MAX_LENGTH,
        help="specifies the maximum length of the word that can be guessed")
    parser.add_argument(
        "-l", "--lives",
        type=int,
        default=MAX_LIVES,
        help="specifies the number of lives you will have throughout the game")

    # as each argument takes exactly one value,
    # the argList must be of even length.
    if len(argList) % 2 != 0:
        error_msg = "missing_value"
        print_error(error_msg)
        raise ValueError(error_msg)

    # parsing the arguments
    args = parser.parse_args(argList)

    # if -m was specified, but the value of args.minimum_length is None,
    # the value 0 was used.
    if ("-m" in argList or "--minimum-length" in argList) and args.minimum_length is None:
        args.minimum_length = -1
    if ("-M" in argList or "--maximum-length" in argList) and args.maximum_length is None:
        args.maximum_length = -1
    if ("-l" in argList or "--lives" in argList) and not args.lives:
        args.lives = -1

    # sanity checks
    if args.minimum_length is not None:
        if args.maximum_length and args.minimum_length > args.maximum_length:
            error_msg = "minimum length value higher than maximum length value"
            print_error(error_msg)
            raise ValueError(error_msg)
        if args.minimum_length < 2:
            error_msg = "minimum length value too low"
            print_error(error_msg)
            raise ValueError(error_msg)

    if args.lives is not None:
        if args.lives > MAX_LIVES:
            error_msg = "that many lives make the game too easy"
            print_error(error_msg)
            raise ValueError(error_msg)
        if args.lives <= 0:
            error_msg = "having less than 1 live is not advised"
            print_error(error_msg)
            raise ValueError(error_msg)

    # ceate config object
    return Configurations(
        lives=args.lives,
        min_length=args.minimum_length,
        max_length=args.maximum_length
    )


def prompt(f: Callable) -> Callable:
    """
    Prompts the user to input a value until either the value is legal
    or an exception different than `ValueError` is raised.
    """
    @wraps(f)
    def inner(*args, **kwargs):
        while True:
            try:
                return f(*args, **kwargs)
            except ValueError:
                continue
    return inner


@prompt
def get_guess(game_state: State) -> Guess:
    user_input = input("Please enter your guess: ")

    if len(user_input) == 1:
        return Guess(guess=user_input)

    if len(user_input) == len(game_state.target_word):
        return Guess(guess=user_input)

    error_msg = "the word to be guessed has a different length"
    print_error(error_msg)
    raise ValueError(error_msg)


@prompt
def get_play_new_game() -> bool:
    user_input = input("Do you want to start a new game? [y/n] ")
    if user_input not in ['y', 'n']:
        error_msg = 'you must answer yes (y) or no (n)'
        print_error(error_msg)
        raise ValueError(error_msg)
    return user_input == 'y'
