import os
import sys


def _cache(f, *args, **kwargs):
    key = (args, frozenset(kwargs.items())) if kwargs else args
    try:
        return f.cache[key]
    except KeyError:
        value = f(*args, **kwargs)
        f.cache[key] = value
        return value


def cached(f):
    f.cache = {}

    def inner(*args, **kwargs):
        return _cache(f, *args, **kwargs)

    return inner


def get_resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource both in dev mode
    and in the PyInstaller bundled executable.
    """
    # NOTE(andrea): this fixes the build on windows.
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.environ.get("_MEIPASS2", os.path.abspath("."))

    return os.path.join(base_path, relative_path)
