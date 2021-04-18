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
