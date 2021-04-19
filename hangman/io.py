import json
from argparse import ArgumentParser
from enum import Enum, unique
from functools import wraps
from typing import Callable, List

from hangman.constants import ANIMATIONS, MAX_LENGTH, MAX_LIVES, MIN_LENGTH
from hangman.data import Configurations, Difficulty, Guess, State, WordList
from hangman.utils import cached


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


@cached
def load_wordlist(
    path: str = './assets/wordlists.json',
    lang: str = 'BRITISH'
) -> WordList:
    with open(path, 'r') as f:
        data = json.load(f)[lang]
    return WordList(**data)


def validate_configuration(
    config: Configurations,
    wordlist: WordList = load_wordlist()
):

    target_list: List[str] = getattr(wordlist, config.difficulty.value, [])

    if max(len(w) for w in target_list) < config.min_length:
        msg = f"The are no words as long as {config.min_length} in the game."
        print_error(msg)
        raise ValueError(msg)


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
    parser.add_argument(
        "-d", "--difficulty",
        default="medium",
        help="specified the difficulty level of the word. Can be: 'easy', 'medium', or 'hard'"
    )

    args = parser.parse_args(argList)

    # sanity checks
    if args.minimum_length is not None:
        if args.maximum_length is not None and args.minimum_length > args.maximum_length:
            error_msg = "minimum length value higher than maximum length value"
            print_error(error_msg)
            raise ValueError(error_msg)
        if args.minimum_length < 2:
            error_msg = "minimum length value too low"
            print_error(error_msg)
            raise ValueError(error_msg)

    if args.maximum_length is not None:
        if args.maximum_length <= 2:
            error_msg = "maximum length value too low"
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

    if args.difficulty is not None:
        if args.difficulty not in ['easy', 'medium', 'hard']:
            error_msg = "Difficulty level is not valid"
            print_error(error_msg)
            raise ValueError(error_msg)

    difficulty_level = Difficulty[args.difficulty.upper()]

    # ceate config object
    out = Configurations(
        lives=args.lives,
        min_length=args.minimum_length,
        max_length=args.maximum_length,
        difficulty=difficulty_level
    )

    validate_configuration(out)

    return out


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
            except ValueError as e:
                print_error(getattr(e, 'message', str(e)))
                continue
    return inner


@prompt
def get_guess(game_state: State) -> Guess:
    user_input = input("Please enter your guess: ").lower()

    if len(user_input) == 0:
        raise ValueError("you must guess a character or the entire word")

    if len(user_input) == 1:
        if not (65 <= ord(user_input) <= 90 or 97 <= ord(user_input) <= 122):
            raise ValueError(
                "the character must be a valid ASCII (65-90 or 97-122)")
        return Guess(guess=user_input)

    if len(user_input) == len(game_state.target_word):
        return Guess(guess=user_input, whole_word=True)

    raise ValueError("the word to be guessed has a different length")


def display(state: State):
    curr_animation = MAX_LIVES - state.current_lives
    if curr_animation >= len(ANIMATIONS):
        # NOTE(andrea): we should use ValueError only as
        # an indicator of failure in input parsing.
        # In this case, if we reach such a state (and we shouldn't)
        # our program should crash.
        raise RuntimeError("Lives is inconsistent with animations.")

    if not state.is_running:
        if state.is_victory:
            print('\nCongratulations, you have guessed the word! 🥳\n')
        else:
            print('\nSorry, you have lost! 😢\n')
        print(f"Word: {' '.join(c for c in state.target_word)}")
    else:
        # print current word based on the list of guesses
        current_word: List[str] = []
        for char in state.target_word:
            try:
                next(g for g in state.guesses if g.guess == char)
                current_word.append(char)
            except StopIteration:
                current_word.append('_')
        print("Word: {}".format(" ".join(current_word)))

    if state.current_guess is not None:
        print("Guess: {}".format(state.current_guess.guess))

    print(ANIMATIONS[curr_animation])


@prompt
def get_play_new_game() -> bool:
    user_input = input("Do you want to start a new game? [y/n] ").lower()
    if user_input not in ['y', 'n']:
        raise ValueError("you must answer yes (y) or no (n)")
    return user_input == 'y'
