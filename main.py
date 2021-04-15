import sys

from hangman.core import State, update_game
from hangman.io import get_guess, get_play_new_game, parse_args


def main():
    config = parse_args(sys.argv[1:])

    is_prog_running = True

    while is_prog_running:
        state = State.from_config(config)

        try:
            while state.is_running:
                try:
                    guess = get_guess(state)
                    state.guesses.append(guess)
                    update_game(state)
                except KeyboardInterrupt:
                    state.is_running = False
                    # NOTE(andrea): this is just for aesthetic purposes
                    print('\n')

            is_prog_running = get_play_new_game()

        except KeyboardInterrupt:
            is_prog_running = False
            # NOTE(andrea): this is just for aesthetic purposes
            print('\n')

    print('Thank your for playing :)')


if __name__ == '__main__':
    main()
