'''

'''
from contextlib import contextmanager
from io import StringIO
from typing import List

import pytest as pt
from hangman.core import Configurations, State, Guess
from hangman.constants import ANIMATIONS, MAX_LIVES


def test_state_construction():
    word = 'hello'
    state = State.new(word, 10)
    assert state.current_word == ['_' for _ in range(len(word))]