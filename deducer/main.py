import argparse
import sys

from .criteria import criteria
from .criterion import PrunableCriteriaCard
from .deducer import Deducer


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

    args = parser.parse_args()

    game_criteria: list[PrunableCriteriaCard] = [
        PrunableCriteriaCard(criteria[_id - 1]) for _id in args.criteria
    ]

    deducer = Deducer(game_criteria)
    deducer.deduce()
    deducer.print_steps()
    print(deducer.possible_codes)

    return 0


if __name__ == "__main__":
    sys.exit(main())
