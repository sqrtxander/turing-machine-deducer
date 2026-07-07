from typing import Callable, cast

from .code import Code
from .criterion import Criterion

_checks = [
    # Criterion 1
    [
        lambda c: c.triangle == 1,
        lambda c: c.triangle > 1,
    ],
    # Criterion 2
    [
        lambda c: c.triangle < 3,
        lambda c: c.triangle == 3,
        lambda c: c.triangle > 3,
    ],
    # Criterion 3
    [
        lambda c: c.square < 3,
        lambda c: c.square == 3,
        lambda c: c.square > 3,
    ],
    # Criterion 4
    [
        lambda c: c.square < 4,
        lambda c: c.square == 4,
        lambda c: c.square > 4,
    ],
    # Criterion 5
    [
        lambda c: c.triangle % 2 == 0,
        lambda c: c.triangle % 2 != 0,
    ],
    # Criterion 6
    [
        lambda c: c.square % 2 == 0,
        lambda c: c.square % 2 != 0,
    ],
    # Criterion 7
    [
        lambda c: c.circle % 2 == 0,
        lambda c: c.circle % 2 != 0,
    ],
    # Criterion 8
    [
        lambda c: c.count(1) == 0,
        lambda c: c.count(1) == 1,
        lambda c: c.count(1) == 2,
        lambda c: c.count(1) == 3,
    ],
    # Criterion 9
    [
        lambda c: c.count(3) == 0,
        lambda c: c.count(3) == 1,
        lambda c: c.count(3) == 2,
        lambda c: c.count(3) == 3,
    ],
    # Criterion 10
    [
        lambda c: c.count(4) == 0,
        lambda c: c.count(4) == 1,
        lambda c: c.count(4) == 2,
        lambda c: c.count(4) == 3,
    ],
    # Criterion 11
    [
        lambda c: c.triangle < c.square,
        lambda c: c.triangle == c.square,
        lambda c: c.triangle > c.square,
    ],
    # Criterion 12
    [
        lambda c: c.triangle < c.circle,
        lambda c: c.triangle == c.circle,
        lambda c: c.triangle > c.circle,
    ],
    # Criterion 13
    [
        lambda c: c.square < c.circle,
        lambda c: c.square == c.circle,
        lambda c: c.square > c.circle,
    ],
    # Criterion 14
    [
        lambda c: c.triangle < c.circle and c.triangle < c.square,
        lambda c: c.square < c.triangle and c.square < c.circle,
        lambda c: c.circle < c.square and c.circle < c.triangle,
    ],
    # Criterion 15
    [
        lambda c: c.triangle > c.circle and c.triangle > c.square,
        lambda c: c.square > c.triangle and c.square > c.circle,
        lambda c: c.circle > c.square and c.circle > c.triangle,
    ],
    # Criterion 16
    [lambda c: c.count_even() >= 2, lambda c: c.count_even() < 2],
    # Criterion 17
    [
        lambda c: c.count_even() == 0,
        lambda c: c.count_even() == 1,
        lambda c: c.count_even() == 2,
        lambda c: c.count_even() == 3,
    ],
    # Criterion 18
    [
        lambda c: c.sum() % 2 == 0,
        lambda c: c.sum() % 2 != 0,
    ],
    # Criterion 19
    [
        lambda c: c.triangle + c.square < 6,
        lambda c: c.triangle + c.square == 6,
        lambda c: c.triangle + c.square > 6,
    ],
    # Criterion 20
    [
        lambda c: len(c.set) == 1,
        lambda c: len(c.set) == 2,
        lambda c: len(c.set) == 3,
    ],
    # Criterion 21
    [
        lambda c: len(c.set) in (1, 3),
        lambda c: len(c.set) == 2,
    ],
    # Criterion 22
    [
        lambda c: c.triangle < c.square < c.circle,
        lambda c: c.triangle > c.square > c.circle,
        lambda c: (
            not (
                c.triangle < c.square < c.circle
                or c.triangle > c.square > c.circle
            )
        ),
    ],
    # Criterion 23
    [
        lambda c: c.sum() < 6,
        lambda c: c.sum() == 6,
        lambda c: c.sum() > 6,
    ],
    # Criterion 24
    [
        lambda c: c.triangle < c.square < c.circle,
        lambda c: (
            c.triangle < c.square >= c.circle
            or c.triangle >= c.square < c.circle
        ),
        lambda c: c.triangle >= c.square >= c.circle,
    ],
]

criteria = [
    Criterion(i, cast(list[Callable[[Code], bool]], checks))
    for i, checks in enumerate(_checks, start=1)
]
