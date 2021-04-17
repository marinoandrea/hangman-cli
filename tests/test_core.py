from hangman.core import Guess, State, update_game


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
