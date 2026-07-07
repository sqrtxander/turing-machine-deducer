import argparse
import sys

from .criteria import criteria
from .criterion import Criterion
from .deducer import Deducer


def criteria_card_arg(s: str) -> list[int]:
    try:
        lst = [int(num) for num in s.split(",")]
    except ValueError as e:
        raise ValueError("Invalid literal for criteria card ID") from e

    if any(num <= 0 or num > 24 for num in lst):
        raise ValueError(
            "Invalid literal for criteria card ID. "
            "Only support IDs in range [1, 24]"
        )

    return lst


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--criteria",
        type=criteria_card_arg,
        required=True,
        help="comma-separated string of criteria card IDs for the challenge.",
    )

    args = parser.parse_args()

    game_criteria: list[Criterion] = [
        criteria[_id - 1] for _id in args.criteria
    ]

    deducer = Deducer(game_criteria)
    deducer.deduce()
    print("DONE")

    return 0


if __name__ == "__main__":
    sys.exit(main())
