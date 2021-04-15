from dataclasses import dataclass
from typing import List, Optional

from hangman.constants import MAX_LENGTH, MAX_LIVES, MIN_LENGTH


@dataclass(frozen=True)
class Configurations:
    """
    The Configurations contains all the configurations that can be done
    through the command line arguments.
    """
    lives: int = MAX_LIVES
    min_length: int = MIN_LENGTH
    max_length: int = MAX_LENGTH


@dataclass
class Guess:
    """
    The Guess contains a certain guess. This could be either one character
    or a guessed string.
    """
    guess: str


@dataclass
class State:
    """
    The state of the system describes the to be guessed word,
    all the wrongly guessed characters, the current progress of the word,
    the number of Lives and the configuration options.
    """
    target_word: str
    current_word: List[str]
    current_lives: int
    guesses: List[Guess]
    current_guess: Optional[Guess]