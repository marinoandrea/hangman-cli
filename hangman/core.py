import random
from typing import List

from hangman.data import Configurations, Difficulty, Guess, State, WordList
from hangman.io import load_wordlist, print_error, print_info


def pick_word(
    min_length: int,
    max_length: int,
    difficulty: Difficulty,
    wordlist: WordList = load_wordlist()
) -> str:
    # NOTE(andrea): this should never fail, so no default should be needed.
    # pick_word should choose a wordlist based on difficulty (and maybe
    # a language configuration?). So, besides from testing, there is no need to
    # pass the list as an argument. We can just use BRITISH as a default.
    target_list: List[str] = getattr(wordlist, difficulty.value, [])

    filtered_target_list = list(filter(
        lambda w: min_length <= len(w) <= max_length, target_list))

    if len(filtered_target_list) <= 0:
        print_error("No word found for given configuration.")
        raise ValueError("No word found for given configuration.")

    return random.choice(filtered_target_list)


def init_state(config: Configurations) -> State:
    target_word = pick_word(
        config.min_length,
        config.max_length,
        config.difficulty,
    )
    return State(target_word=target_word, current_lives=config.lives)


def is_word_found(game_state: State) -> bool:
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
        game_state.is_running = False
        game_state.is_victory = True

    def take_life():
        game_state.current_lives -= 1
        if game_state.current_lives == 0:
            game_state.is_running = False
            game_state.is_victory = False

    if guess.whole_word:
        if game_state.target_word == guess.guess:
            win()
        else:
            take_life()
    else:
        if game_state.target_word.find(guess.guess) != -1:
            if is_word_found(game_state):
                win()
        else:
            take_life()
