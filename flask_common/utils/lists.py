from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from builtins import range


def grouper(n, iterable):
    # e.g. 2, [1, 2, 3, 4, 5] -> [[1, 2], [3, 4], [5]]
    return [iterable[i : i + n] for i in range(0, len(iterable), n)]
