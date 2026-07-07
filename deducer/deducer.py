from .criterion import Criterion


class Deducer:
    def __init__(self, criteria_cards: list[Criterion]) -> None:
        self.criteria_cards = criteria_cards

    def deduce(self) -> None:
        self.superfluity()

    def superfluity(self) -> None:
        for card_1 in self.criteria_cards:
            for i, codes_1 in enumerate(card_1.option_codes):
                for card_2 in self.criteria_cards:
                    if card_1 == card_2:
                        continue
                    for codes_2 in card_2.option_codes:
                        if codes_1.issubset(codes_2):
                            print(
                                f"{card_1} option {i} ruled "
                                "out due to superfluity. "
                                f"Makes {card_2} superfluous."
                            )
