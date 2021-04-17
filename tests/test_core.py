from hangman.core import Guess, State, update_game


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
