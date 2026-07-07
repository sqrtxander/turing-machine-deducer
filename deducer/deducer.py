from .code import all_codes
from .criterion import Criterion


class Deducer:
    def __init__(self, criteria_cards: list[Criterion]) -> None:
        self.criteria_cards = criteria_cards
        self.possible_codes = set(all_codes())

    def deduce(self) -> None:
        self.superfluity()

    def superfluity(self) -> None:
        for card_1 in self.criteria_cards:
            for (
                i,
                (codes_1, complement_codes_1),
            ) in enumerate(
                zip(
                    card_1.possible_codes,
                    card_1.complement_possible_codes,
                    strict=True,
                )
            ):
                for card_2 in self.criteria_cards:
                    if card_1 == card_2:
                        continue
                    for (
                        codes_2,
                        complement_codes_2,
                    ) in zip(
                        card_2.possible_codes,
                        card_2.complement_possible_codes,
                        strict=True,
                    ):
                        if (
                            not codes_1.intersection(complement_codes_2)
                        ) and codes_1.issubset(codes_2):
                            self.possible_codes &= complement_codes_1
                            print(
                                f"{card_1} option {i} ruled "
                                "out due to superfluity. "
                                f"Makes {card_2} superfluous. "
                                f"Now there are {len(self.possible_codes)} "
                                "possible codes."
                            )
