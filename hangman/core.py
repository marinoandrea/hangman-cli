from hangman.data import Configurations, Difficulty, Guess, State
from hangman.io import display, print_info


def pick_word(
    min_length: int, max_length: int, max_difficulty: Difficulty
) -> str:
    raise NotImplementedError()


def init_state(config: Configurations) -> State:
    target_word = pick_word(
        config.min_length,
        config.max_length,
        config.difficulty
    )
    return State(target_word=target_word, current_lives=config.lives)


def _is_word_found(game_state: State) -> bool:
    for c in game_state.target_word:
        try:
            next(g for g in game_state.guesses if g.guess == c)
        except StopIteration:
            return False
    return True


def update_game(game_state: State, guess: Guess):
    try:
        next(g for g in game_state.guesses if g.guess == guess.guess)
        print_info("you already input this, try a different word/character")
        return
    except StopIteration:
        pass

    game_state.current_guess = guess
    game_state.guesses.append(guess)

    def win():
        game_state.is_over = True
        game_state.is_victory = True

    def take_life():
        game_state.current_lives -= 1
        if game_state.current_lives == 0:
            game_state.is_over = True
            game_state.is_victory = False

    if guess.whole_word:
        if game_state.target_word == guess.guess:
            win()
        else:
            take_life()
    else:
        if game_state.target_word.find(guess.guess) != -1:
            if _is_word_found(game_state):
                win()
        else:
            take_life()

    display(game_state)
