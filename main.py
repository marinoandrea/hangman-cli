import sys

from hangman.core import init_state, update_game
from hangman.io import (display, get_guess, get_play_new_game, parse_args,
                        print_info, validate_configuration)


def main():
    try:
        config = parse_args(sys.argv[1:])
        is_prog_running = True
    except ValueError:
        print_info('Please try to start the game with different arguments.')
        is_prog_running = False

    while is_prog_running:
        state = init_state(config)
        display(state)

        try:
            while state.is_running:
                try:
                    guess = get_guess(state)
                    update_game(state, guess)
                    display(state)
                except (KeyboardInterrupt, EOFError):
                    state.is_running = False
                    # NOTE(andrea): this is just for aesthetic purposes
                    print('\n')

            is_prog_running = get_play_new_game()

        except (KeyboardInterrupt, EOFError):
            is_prog_running = False
            # NOTE(andrea): this is just for aesthetic purposes
            print('\n')

    print('Thank your for playing 😀')


if __name__ == '__main__':
    main()
