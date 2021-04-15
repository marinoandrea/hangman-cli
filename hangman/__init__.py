from dataclasses import dataclass
from enum import Enum, unique
from typing import List
from argparse import ArgumentParser


@unique
class colors(Enum):
    value: str
    RED = '\033[31m'
    END = '\033[0m'
    BLUE = '\033[96m'

    def __str__(self) -> str:
        return self.value

MAX_LIVES: int = 10

@dataclass
class Configurations:
    """
    The Configurations contains all the configurations that can be done
    through the command line arguments.
    """
    lives: int
    min_length: int
    max_length: int

    def __init__(self, lives: int = 10, min_length: int = 2, max_length: int = 2000):
        self.lives = lives
        self.min_length = min_length
        self.max_length = max_length


class State:
    """
    The state of the system describes the to be guessed word,
    all the wrongly guessed characters, the current progress of the word,
    the number of Lives and the configuration options.
    """

    def __init__(self, config: Configurations):
        self.lives = config.lives


def print_error(string: str):
    print(f"{colors.RED}{string}{colors.END}")


def print_info(string: str):
    print(f"{colors.BLUE}{string}{colors.END}")

def parse_args(argList: List[str]) -> Configurations:
    # specifying the argument parser
    parser = ArgumentParser(description="configuration of hangman game")
    parser.add_argument("-m", "--minimum-length",
        type=int, 
        help="specifies the minimum length of the word that can be guessed")
    parser.add_argument("-M","--maximum-length", 
        type=int,
        help="specifies the maximum length of the word that can be guessed")
    parser.add_argument("-l", "--lives",
        type=int,
        help="specifies the number of lives you will have throughout the game")

    # as each argument takes exactly one value, the argList must be of even length.
    if len(argList) % 2 != 0 :
        print_error("error: missing value")
        return None
    
    # parsing the arguments
    args = parser.parse_args(argList)

    # if -m was specified, but the value of args.minimum_length is None, the value 0 was used.
    if ("-m" in argList or "--minimum-length" in argList) and not args.minimum_length:
        args.minimum_length = -1
    if ("-M" in argList or "--maximum-length" in argList) and not args.maximum_length:
        args.maximum_length = -1
    if ("-l" in argList or "--lives" in argList) and not args.lives:
        args.lives = -1

    # sanity checks
    if args.minimum_length:
        if args.maximum_length and args.minimum_length > args.maximum_length:
            print_error("error: minimum length value higher than maximum length value")
            return None
        
        if args.minimum_length < 2:
            print_error("error: minimum length value too low")
            return None
    if args.lives:
        if args.lives > MAX_LIVES:
            print_error("error: that many lives make the game too easy")
            return None
        if args.lives <= 0:
            print_error("error: having less than 1 live is not advised")

    # ceate config object
    return Configurations(lives = args.lives, min_length=args.minimum_length, max_length=args.maximum_length)


