from dataclasses import dataclass, field
from enum import Enum, unique
from typing import List

from hangman.constants import MAX_LENGTH, MAX_LIVES, MIN_LENGTH


@unique
class Difficulty(Enum):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'


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
    current_lives: int
    guesses: List[Guess] = field(default_factory=lambda: [])
    is_running: bool = True

    @staticmethod
    def from_config(config: Configurations) -> 'State':
        target_word = pick_word(
            config.min_length,
            config.max_length,
            config.difficulty
        )
        return State(
            target_word=target_word,
            current_lives=config.lives,
        )


def update_game(game_state: State):
    raise NotImplementedError()


def pick_word(
    min_length: int, max_length: int, max_difficulty: Difficulty
) -> str:
    raise NotImplementedError()
