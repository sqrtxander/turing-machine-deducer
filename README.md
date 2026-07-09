# Turing Machine Deducer

## About

This is a tool designed to show logical deduction steps that can be made in the logical deduction game [Turing Machine](https://www.scorpionmasque.com/en/turingmachine).

## Features

- CLI tool to make deductions for arbitrary criteria card combinations
- Error handling for impossible criteria card combinations

## Limitations

### Zero-queryable Challenges

Denote a criteria card combination as a challenge.

Challenge are considered "easy" if they only contain criteria cards in the inclusive range 1 to 25.

Challenge are considered "hard" if they contain at least one verifier in the inclusive range 26 to 48.

BGG user @mg6maciej in [this forum post](https://boardgamegeek.com/thread/3166002/no-question-challenges-5-cards-classic-easy-mode-o/page/2) provided all challenges that can be solved with 0 queries, with the exclusion of 6-verifier hard challenges. We will denote this set as "zero-queryable challenges", and use the provided challenges as our source of truth.

We first consider the subset of 4-verifier zero-queryable easy challenges. After running every challenges through the deducer, there were 50 challenges that were not able to be solved. These challenges are shown in [unsolved/easy_4.txt](unsolved/easy_4.txt).

Further subsets will be considered after most of the currently unsolved 4-verifier zero-queryable easy challenges are resolved.

### n-queryable Challenges (n > 0)

The deducer is primarily designed for zero-queryable challenges.

Define n-queryable challenges as challenges that require at least n queries to solve

Considerations for n-queryable challenges, for positive n, may include:
- suggesting codes to query
- accepting user input for query results

## Example

```bash
python -m deducer.main --criteria 1,6,8,15,19
```

Criteria card IDs are input through the `--criteria` flag, separated by commas.

The above criteria card combination outputs these deduction steps.
```
c01 [ triangle_eq_1 | triangle_gt_1 ]
c06 [ square_even | square_odd ]
c08 [ zero_ones | one_one | two_ones | three_ones ]
c15 [ triangle_gt_circle_square | square_gt_triangle_circle | circle_gt_square_triangle ]
c19 [ triangle_plus_square_lt_6 | triangle_plus_square_eq_6 | triangle_plus_square_gt_6 ]
BEGIN CHECKING c08_num_ones__zero_ones against c01_triangle_cmp_1
    zero_ones is disjoint from triangle_eq_1,
    zero_ones is contained by triangle_gt_1.
    => c01_triangle_cmp_1 is superfluous.
    Therefore c08_num_ones__zero_ones is ruled out.
END CHECKING
BEGIN CHECKING c08_num_ones__three_ones against c01_triangle_cmp_1
    three_ones is contained by triangle_eq_1,
    three_ones is disjoint from triangle_gt_1.
    => c01_triangle_cmp_1 is superfluous.
    Therefore c08_num_ones__three_ones is ruled out.
END CHECKING
BEGIN CHECKING c15_highest__triangle_gt_circle_square against c01_triangle_cmp_1
    triangle_gt_circle_square is disjoint from triangle_eq_1,
    triangle_gt_circle_square is contained by triangle_gt_1.
    => c01_triangle_cmp_1 is superfluous.
    Therefore c15_highest__triangle_gt_circle_square is ruled out.
END CHECKING
BEGIN CHECKING c19_triangle_plus_square_cmp_6__triangle_plus_square_gt_6 against c01_triangle_cmp_1
    triangle_plus_square_gt_6 is disjoint from triangle_eq_1,
    triangle_plus_square_gt_6 is contained by triangle_gt_1.
    => c01_triangle_cmp_1 is superfluous.
    Therefore c19_triangle_plus_square_cmp_6__triangle_plus_square_gt_6 is ruled out.
END CHECKING
BEGIN CHECKING c08_num_ones__two_ones against c01_triangle_cmp_1
    Since (square_gt_triangle_circle OR circle_gt_square_triangle) is known true,
    two_ones is contained by triangle_eq_1,
    two_ones is disjoint from triangle_gt_1.
    => c01_triangle_cmp_1 is superfluous.
    Therefore c08_num_ones__two_ones is ruled out.
END CHECKING
c08_num_ones has only one remaining criterion.
Therefore c08_num_ones__one_one is true.
BEGIN CHECKING c15_highest__circle_gt_square_triangle against c19_triangle_plus_square_cmp_6
    Since one_one is known true,
    circle_gt_square_triangle is contained by triangle_plus_square_lt_6,
    circle_gt_square_triangle is disjoint from triangle_plus_square_eq_6,
    circle_gt_square_triangle is disjoint from triangle_plus_square_gt_6.
    => c19_triangle_plus_square_cmp_6 is superfluous.
    Therefore c15_highest__circle_gt_square_triangle is ruled out.
END CHECKING
c15_highest has only one remaining criterion.
Therefore c15_highest__square_gt_triangle_circle is true.
c01 [ triangle_eq_1 | triangle_gt_1 ]
c06 [ square_even | square_odd ]
c08 [ one_one ]
c15 [ square_gt_triangle_circle ]
c19 [ triangle_plus_square_lt_6 | triangle_plus_square_eq_6 ]
BEGIN ASSUMING c01_triangle_cmp_1__triangle_gt_1
    BEGIN CHECKING c19_triangle_plus_square_cmp_6__triangle_plus_square_lt_6 against c06_square_parity
        Since triangle_gt_1 AND square_gt_triangle_circle is known true,
        triangle_plus_square_lt_6 is disjoint from square_even,
        triangle_plus_square_lt_6 is contained by square_odd.
        => c06_square_parity is superfluous.
        Therefore c19_triangle_plus_square_cmp_6__triangle_plus_square_lt_6 is ruled out.
    END CHECKING
    BEGIN CHECKING c19_triangle_plus_square_cmp_6__triangle_plus_square_eq_6 against c06_square_parity
        Since triangle_gt_1 AND square_gt_triangle_circle is known true,
        triangle_plus_square_eq_6 is contained by square_even,
        triangle_plus_square_eq_6 is disjoint from square_odd.
        => c06_square_parity is superfluous.
        Therefore c19_triangle_plus_square_cmp_6__triangle_plus_square_eq_6 is ruled out.
    END CHECKING
    c19_triangle_plus_square_cmp_6 has no possible criteria.
    Therefore our assumption was wrong, and c01_triangle_cmp_1__triangle_gt_1 is ruled out.
END ASSUMING
c01_triangle_cmp_1 has only one remaining criterion.
Therefore c01_triangle_cmp_1__triangle_eq_1 is true.
c01 [ triangle_eq_1 ]
c06 [ square_even | square_odd ]
c08 [ one_one ]
c15 [ square_gt_triangle_circle ]
c19 [ triangle_plus_square_lt_6 | triangle_plus_square_eq_6 ]
BEGIN ASSUMING c06_square_parity__square_even
    BEGIN CHECKING c01_triangle_cmp_1__triangle_eq_1 against c19_triangle_plus_square_cmp_6
        Since square_even is known true,
        triangle_eq_1 is contained by triangle_plus_square_lt_6,
        triangle_eq_1 is disjoint from triangle_plus_square_eq_6,
        triangle_eq_1 is disjoint from triangle_plus_square_gt_6.
        => c19_triangle_plus_square_cmp_6 is superfluous.
        Therefore c01_triangle_cmp_1__triangle_eq_1 is ruled out.
    END CHECKING
    c01_triangle_cmp_1 has no possible criteria.
    Therefore our assumption was wrong, and c06_square_parity__square_even is ruled out.
END ASSUMING
c06_square_parity has only one remaining criterion.
Therefore c06_square_parity__square_odd is true.
c01 [ triangle_eq_1 ]
c06 [ square_odd ]
c08 [ one_one ]
c15 [ square_gt_triangle_circle ]
c19 [ triangle_plus_square_lt_6 | triangle_plus_square_eq_6 ]
BEGIN ASSUMING c19_triangle_plus_square_cmp_6__triangle_plus_square_eq_6
    BEGIN CHECKING c01_triangle_cmp_1__triangle_eq_1 against c06_square_parity
        Since triangle_plus_square_eq_6 is known true,
        triangle_eq_1 is disjoint from square_even,
        triangle_eq_1 is contained by square_odd.
        => c06_square_parity is superfluous.
        Therefore c01_triangle_cmp_1__triangle_eq_1 is ruled out.
    END CHECKING
    c01_triangle_cmp_1 has no possible criteria.
    Therefore our assumption was wrong, and c19_triangle_plus_square_cmp_6__triangle_plus_square_eq_6 is ruled out.
END ASSUMING
c19_triangle_plus_square_cmp_6 has only one remaining criterion.
Therefore c19_triangle_plus_square_cmp_6__triangle_plus_square_lt_6 is true.
c01 [ triangle_eq_1 ]
c06 [ square_odd ]
c08 [ one_one ]
c15 [ square_gt_triangle_circle ]
c19 [ triangle_plus_square_lt_6 ]
All criteria cards deduced.
The code is 132.
```
