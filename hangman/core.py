from hangman.data import Configurations, Difficulty, Guess, State, WordList
from hangman.io import display, print_info
import random

def pick_word(
    min_length: int, max_length: int, max_difficulty: Difficulty, word_list: WordList
) -> str:
    target_list = word_list.easy if max_difficulty == Difficulty.EASY else word_list.medium if max_difficulty == Difficulty.MEDIUM else word_list.hard
    filtered_target_list = list(filter(lambda w: len(w) >= min_length and len(w) <= max_length, target_list))
    if len(filtered_target_list) <= 0:
        raise ValueError("No word found for given configuration.")
    return filtered_target_list[random.randint(0, len(filtered_target_list) - 1)]



def init_state(config: Configurations) -> State:
    target_word = pick_word(
        config.min_length,
        config.max_length,
        config.difficulty,
        config.word_list
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
            if _is_word_found(game_state):
                win()
        else:
            take_life()
