import argparse

from .criteria import criteria


def criteria_card_arg(s: str):
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--criteria",
        type=criteria_card_arg,
        required=True,
        help="comma-separated string of criteria card IDs for the challenge.",
    )

    args = parser.parse_args()

    game_criteria = [criteria[_id - 1] for _id in args.criteria]

    for criteria_card in game_criteria:
        print(criteria_card)


if __name__ == "__main__":
    main()
