import pytest
from hangman.core import is_word_found, pick_word, update_game
from hangman.data import Difficulty, Guess, State, WordList


def test_update_game():

    # wrong char guess path
    state = State(
        target_word="penguin",
        current_lives=2,
    )
    update_game(state, Guess('x'))

    # will fail if state is not updated
    next(g for g in state.guesses if g.guess == 'x')
    assert state.current_guess == Guess('x')
    # lives are expected to change
    assert state.current_lives == 1

    # right char guess path
    state = State(
        target_word="penguin",
        current_lives=2,
    )
    update_game(state, Guess('p'))

    # lives are not expected to change
    assert state.current_lives == 2

    # wrong word guess path
    state = State(
        target_word="penguin",
        current_lives=2,
    )
    update_game(state, Guess(guess='penguix', whole_word=True))

    # will fail if state is not updated
    next(g for g in state.guesses if g.guess == 'penguix')
    assert state.current_guess == Guess(guess='penguix', whole_word=True)
    # lives are expected to change
    assert state.current_lives == 1

    # right word guess path
    state = State(
        target_word="penguin",
        current_lives=2,
    )
    update_game(state, Guess(guess='penguin', whole_word=True))

    # lives are expected to change
    assert state.current_lives == 2
    assert not state.is_running
    assert state.is_victory

    # wrong char lose path
    state = State(
        target_word="penguin",
        current_lives=1,
    )
    update_game(state, Guess(guess='x'))

    # lives are expected to change
    assert state.current_lives == 0
    assert not state.is_running
    assert not state.is_victory

    # wrong word lose path
    state = State(
        target_word="penguin",
        current_lives=1,
    )
    update_game(state, Guess(guess='penguix', whole_word=True))

    # lives are expected to change
    assert state.current_lives == 0
    assert not state.is_running
    assert not state.is_victory

    # word is found by char guess
    state = State(
        target_word="ace",
        current_lives=1,
        guesses=[Guess('a'), Guess('c')]
    )
    update_game(state, Guess(guess='e'))

    assert state.current_lives == 1
    assert not state.is_running
    assert state.is_victory

    # repeated input
    state = State(
        target_word="ace",
        current_lives=1,
        guesses=[Guess('a'), Guess('c')]
    )
    clone = State(
        target_word="ace",
        current_lives=1,
        guesses=[Guess('a'), Guess('c')]
    )

    update_game(state, Guess(guess='a'))

    assert state == clone


def test_pick_word():
    easy_word = pick_word(1, 100, Difficulty.EASY, WordList(
        easy=["hello"], medium=["world"], hard=["hard"]))
    assert easy_word == "hello"

    medium_word = pick_word(1, 100, Difficulty.MEDIUM, WordList(
        easy=["hello"], medium=["world"], hard=["hard"]))
    assert medium_word == "world"

    hard_word = pick_word(1, 100, Difficulty.HARD, WordList(
        easy=["hello"], medium=["world"], hard=["hard"]))
    assert hard_word == "hard"

    # test for empty list
    with pytest.raises(ValueError):
        hard_word = pick_word(1, 100, Difficulty.HARD, WordList(
            easy=["hello"], medium=["world"], hard=[]))


def test_pick_word_bad_config():
    with pytest.raises(ValueError):
        pick_word(1, 2, Difficulty.EASY, WordList(
            easy=["hello"], medium=["world"], hard=["hard"]))

    with pytest.raises(ValueError):
        pick_word(1, 2, Difficulty.EASY, WordList(
            easy=[], medium=["world"], hard=["hard"]))


def test_is_word_found():
    state = State(
        target_word="ace",
        current_lives=2,
        guesses=[Guess('a'), Guess('c'), Guess('e')]
    )
    assert is_word_found(state)

    state = State(
        target_word="ace",
        current_lives=2,
        guesses=[Guess('a'), Guess('c'), Guess('x')]
    )
    assert not is_word_found(state)
