from dataclasses import dataclass, field
from enum import Enum, unique
from typing import List, Optional

from hangman.constants import MAX_LENGTH, MAX_LIVES, MIN_LENGTH


@unique
class Difficulty(Enum):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'


@dataclass
class WordList:
    """
    Describes a list of words divided into three categories: easy, medium, and hard.
    """
    easy: List[str]
    medium: List[str]
    hard: List[str]


@dataclass(frozen=True)
class Configurations:
    """
    The Configurations contains all the configurations that can be done
    through the command line arguments.
    """
    lives: int = MAX_LIVES
    min_length: int = MIN_LENGTH
    max_length: int = MAX_LENGTH
    difficulty: Difficulty = Difficulty.MEDIUM
    word_list: Optional[WordList] = WordList(easy=["Bye"], medium=["Difficult"], hard=["Zyuganov"])


@dataclass(eq=True, frozen=True)
class Guess:
    """
    The Guess contains a certain guess. This could be either one character
    or a guessed string.
    """
    guess: str
    whole_word: bool = False


@dataclass
class State:
    """
    The state of the system describes the to be guessed word,
    all the wrongly guessed characters, the current progress of the word,
    the number of Lives and the configuration options.
    """
    target_word: str
    current_lives: int
    current_guess: Optional[Guess] = None
    guesses: List[Guess] = field(default_factory=lambda: [])
    is_running: bool = True
    is_victory: bool = False