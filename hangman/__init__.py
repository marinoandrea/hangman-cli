from dataclasses import dataclass
from enum import Enum, unique


@unique
class colors(Enum):
    value: str
    RED = '\033[31m'
    END = '\033[0m'
    BLUE = '\033[96m'

    def __str__(self) -> str:
        return self.value


@dataclass
class Configurations:
    """
    The Configurations contains all the configurations that can be done
    through the command line arguments.
    """
    lives: int
    min_length: int
    max_length: int


class State:
    """
    The state of the system describes the to be guessed word,
    all the wrongly guessed characters, the current progress of the word,
    the number of Lives and the configuration options.
    """

    def __init__(self, configurations: Configurations):
        self.lives = configurations.lives


def print_error(string: str):
    print(f"{colors.RED}{string}{colors.END}")


def print_info(string: str):
    print(f"{colors.BLUE}{string}{colors.END}")
