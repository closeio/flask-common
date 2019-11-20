from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from flask_common.enum import Enum


class TestEnum(Enum):
    A = 'a'
    B = 'b'


def test_enum():
    # Fetch twice to ensure cache is correct
    assert list(TestEnum.values()) == ['a', 'b']
    assert list(TestEnum.values()) == ['a', 'b']
    assert TestEnum.choices() == [('a', 'A'), ('b', 'B')]
    assert TestEnum.choices() == [('a', 'A'), ('b', 'B')]
