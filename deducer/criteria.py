from typing import Callable, cast

from .code import Code
from .criterion import CriteriaCard

_criteria = [
    (
        "c01_triangle_cmp_1",
        {
            "triangle_eq_1": lambda c: c.triangle == 1,
            "triangle_gt_1": lambda c: c.triangle > 1,
        },
    ),
    (
        "c02_triangle_cmp_3",
        {
            "triangle_lt_3": lambda c: c.triangle < 3,
            "triangle_eq_3": lambda c: c.triangle == 3,
            "triangle_gt_3": lambda c: c.triangle > 3,
        },
    ),
    (
        "c03_square_cmp_3",
        {
            "square_lt_3": lambda c: c.square < 3,
            "square_eq_3": lambda c: c.square == 3,
            "square_gt_3": lambda c: c.square > 3,
        },
    ),
    (
        "c04_square_cmp_4",
        {
            "square_lt_4": lambda c: c.square < 4,
            "square_eq_4": lambda c: c.square == 4,
            "square_gt_4": lambda c: c.square > 4,
        },
    ),
    (
        "c05_triangle_parity",
        {
            "triangle_even": lambda c: c.triangle % 2 == 0,
            "triangle_odd": lambda c: c.triangle % 2 != 0,
        },
    ),
    (
        "c06_square_parity",
        {
            "square_even": lambda c: c.square % 2 == 0,
            "square_odd": lambda c: c.square % 2 != 0,
        },
    ),
    (
        "c07_circle_parity",
        {
            "circle_even": lambda c: c.circle % 2 == 0,
            "circle_odd": lambda c: c.circle % 2 != 0,
        },
    ),
    (
        "c08_num_ones",
        {
            "zero_ones": lambda c: c.count(1) == 0,
            "one_one": lambda c: c.count(1) == 1,
            "two_ones": lambda c: c.count(1) == 2,
            "three_ones": lambda c: c.count(1) == 3,
        },
    ),
    (
        "c09_num_threes",
        {
            "zero_threes": lambda c: c.count(3) == 0,
            "one_three": lambda c: c.count(3) == 1,
            "two_threes": lambda c: c.count(3) == 2,
            "three_threes": lambda c: c.count(3) == 3,
        },
    ),
    (
        "c10_num_fours",
        {
            "zero_fours": lambda c: c.count(4) == 0,
            "one_four": lambda c: c.count(4) == 1,
            "two_fours": lambda c: c.count(4) == 2,
            "three_fours": lambda c: c.count(4) == 3,
        },
    ),
    (
        "c11_triangle_cmp_square",
        {
            "triangle_lt_square": lambda c: c.triangle < c.square,
            "triangle_eq_square": lambda c: c.triangle == c.square,
            "triangle_gt_square": lambda c: c.triangle > c.square,
        },
    ),
    (
        "c12_triangle_cmp_circle",
        {
            "triangle_lt_circle": lambda c: c.triangle < c.circle,
            "triangle_eq_circle": lambda c: c.triangle == c.circle,
            "triangle_gt_circle": lambda c: c.triangle > c.circle,
        },
    ),
    (
        "c13_square_cmp_circle",
        {
            "square_lt_circle": lambda c: c.square < c.circle,
            "square_eq_circle": lambda c: c.square == c.circle,
            "square_gt_circle": lambda c: c.square > c.circle,
        },
    ),
    (
        "c14_lowest",
        {
            "triangle_lt_circle_square": lambda c: (
                c.triangle < c.circle and c.triangle < c.square
            ),
            "square_lt_triangle_circle": lambda c: (
                c.square < c.triangle and c.square < c.circle
            ),
            "circle_lt_square_triangle": lambda c: (
                c.circle < c.square and c.circle < c.triangle
            ),
        },
    ),
    (
        "c15_highest",
        {
            "triangle_gt_circle_square": lambda c: (
                c.triangle > c.circle and c.triangle > c.square
            ),
            "square_gt_triangle_circle": lambda c: (
                c.square > c.triangle and c.square > c.circle
            ),
            "circle_gt_square_triangle": lambda c: (
                c.circle > c.square and c.circle > c.triangle
            ),
        },
    ),
    (
        "c16_even_cmp_odd",
        {
            "even_gt_odd": lambda c: c.count_even() >= 2,
            "even_lt_odd": lambda c: c.count_even() < 2,
        },
    ),
    (
        "c17_num_even",
        {
            "zero_evens": lambda c: c.count_even() == 0,
            "one_even": lambda c: c.count_even() == 1,
            "two_evens": lambda c: c.count_even() == 2,
            "three_evens": lambda c: c.count_even() == 3,
        },
    ),
    (
        "c18_sum_parity",
        {
            "sum_even": lambda c: c.sum() % 2 == 0,
            "sum_odd": lambda c: c.sum() % 2 != 0,
        },
    ),
    (
        "c19_triangle_plus_square_cmp_6",
        {
            "triangle_plus_square_lt_6": lambda c: c.triangle + c.square < 6,
            "triangle_plus_square_eq_6": lambda c: c.triangle + c.square == 6,
            "triangle_plus_square_gt_6": lambda c: c.triangle + c.square > 6,
        },
    ),
    (
        "c20_repetition",
        {
            "one_triple": lambda c: len(c.set) == 1,
            "one_double": lambda c: len(c.set) == 2,
            "no_repeat": lambda c: len(c.set) == 3,
        },
    ),
    (
        "c21_has_double",
        {
            "no_double": lambda c: len(c.set) in (1, 3),
            "one_double": lambda c: len(c.set) == 2,
        },
    ),
    (
        "c22_order",
        {
            "asc": lambda c: c.triangle < c.square < c.circle,
            "desc": lambda c: c.triangle > c.square > c.circle,
            "no_order": lambda c: (
                not (
                    c.triangle < c.square < c.circle
                    or c.triangle > c.square > c.circle
                )
            ),
        },
    ),
    (
        "c23_sum_cmp_6",
        {
            "sum_lt_6": lambda c: c.sum() < 6,
            "sum_eq_6": lambda c: c.sum() == 6,
            "sum_gt_6": lambda c: c.sum() > 6,
        },
    ),
    (
        "c24_len_asc_sequence",
        {
            "three_asc": lambda c: c.triangle + 1 == c.square == c.circle - 1,
            "two_asc": lambda c: (
                c.triangle + 1 == c.square != c.circle - 1
                or c.triangle + 1 != c.square == c.circle - 1
            ),
            "no_asc": lambda c: c.triangle + 1 != c.square != c.circle - 1,
        },
    ),
]

criteria = [
    CriteriaCard(_id, cast(dict[str, Callable[[Code], bool]], _checks))
    for _id, _checks in _criteria
]
