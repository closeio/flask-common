from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


def freeze(x):
    """Convert dicts and lists to frozensets of key/index, value pairs, recursively.

    Good for using complex python data structures in sets or dict keys.
    It is idempotent in a sense that freeze(freeze(x)) == freeze(x).
    """
    if isinstance(x, dict):
        return frozenset((k, freeze(v)) for k, v in x.items())
    if isinstance(x, list):
        return frozenset(enumerate(freeze(e) for e in x))
    return x


def dict_with_class(obj):
    """Just like obj.__dict__, but includes data (non-function) class attributes."""
    d = {}
    for cls in reversed(obj.__class__.__mro__):
        for k, v in cls.__dict__.items():
            if not (k.startswith('_') or callable(v)):
                d[k] = v
    d.update(obj.__dict__)
    return d
