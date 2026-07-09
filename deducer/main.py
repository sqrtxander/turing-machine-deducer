import argparse
import sys

from .criteria import criteria
from .criterion import PrunableCriteriaCard
from .deducer import Deducer
from .errors import UnsolvableError


def _criteria_card_arg(s: str) -> list[int]:
    try:
        lst = [int(num) for num in s.split(",")]
    except ValueError as e:
        raise ValueError("Invalid literal for criteria card ID") from e

    if any(num <= 0 or num > 48 for num in lst):
        raise ValueError(
            "Invalid literal for criteria card ID. "
            "Only support IDs in range [1, 48]"
        )

    return lst


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--criteria",
        type=_criteria_card_arg,
        required=True,
        help="comma-separated string of criteria card IDs for the challenge.",
    )
    parser.add_argument(
        "--output-on-fail",
        action="store_true",
        required=False,
        help="only output the criteria ids when failing, else output nothing",
    )

    args = parser.parse_args()

    game_criteria: list[PrunableCriteriaCard] = [
        PrunableCriteriaCard(criteria[_id - 1]) for _id in args.criteria
    ]

    deducer = Deducer(game_criteria)
    error = False
    try:
        solved = deducer.deduce()
    except UnsolvableError:
        error = True

    if not args.output_on_fail:
        deducer.print_steps()

    if (error or not solved) and args.output_on_fail:
        print(", ".join([str(_id) for _id in args.criteria]))

    return int(error)


if __name__ == "__main__":
    sys.exit(main())
