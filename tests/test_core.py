from hangman.core import Guess, State, update_game, pick_word
from hangman.data import Difficulty, WordList
import pytest

def test_update_game():

    # wrong guess path
    state = State(
        target_word="penguin",
        current_lives=2,
    )
    update_game(state, Guess('x'))

    # will fail if state is not updated
    next(g for g in state.guesses if g.guess == 'x')
    # lives are expected to change
    assert state.current_lives == 1

    # right guess path
    state = State(
        target_word="penguin",
        current_lives=2,
    )
    update_game(state, Guess('p'))

    # will fail if state is not updated
    next(g.guess for g in state.guesses if g.guess == 'p')
    # lives are not expected to change
    assert state.current_lives == 2


def test_pick_word():
    easy_word = pick_word(1, 100, Difficulty.EASY, WordList(easy=["hello"], medium=["world"], hard=["hard"]))
    assert easy_word == "hello"

    medium_word = pick_word(1, 100, Difficulty.MEDIUM, WordList(easy=["hello"], medium=["world"], hard=["hard"]))
    assert medium_word == "world"

    hard_word = pick_word(1, 100, Difficulty.HARD, WordList(easy=["hello"], medium=["world"], hard=["hard"]))
    assert hard_word == "hard"


def test_pick_word_bad_config():
    with pytest.raises(ValueError):
        pick_word(1, 2, Difficulty.EASY, WordList(easy=["hello"], medium=["world"], hard=["hard"]))

    with pytest.raises(ValueError):
        pick_word(1, 2, Difficulty.EASY, WordList(easy=[], medium=["world"], hard=["hard"]))
