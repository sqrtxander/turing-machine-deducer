import itertools
from typing import override

from .code import Code, all_codes
from .criterion import CriteriaCard, Criterion


class Deducer:
    @override
    def __init__(self, criteria_cards: list[CriteriaCard]) -> None:
        self.criteria_cards: list[CriteriaCard] = criteria_cards
        self.card_criterion_options: list[list[Criterion]] = [
            card.criteria.copy() for card in self.criteria_cards
        ]
        self.possible_codes: set[Code] = set(all_codes())
        self.steps: list[str] = []

    def print_steps(self) -> None:
        print("\n\n".join(self.steps))

    def deduce(self) -> None:
        self.superfluity()
        self.uniqueness()

    def superfluity(self) -> None:
        for testing_card, testing_options in zip(
            self.criteria_cards, self.card_criterion_options, strict=True
        ):
            for other_card in self.criteria_cards:
                if testing_card is other_card:
                    continue
                for testing_criterion in testing_card.criteria:
                    if testing_criterion not in testing_options:
                        continue
                    for other_criteria in other_card.criteria:
                        if (
                            not testing_criterion.possible_codes.intersection(
                                other_criteria.complement_possible_codes
                            )
                        ) and testing_criterion.possible_codes.issubset(
                            other_criteria.possible_codes
                        ):
                            self.possible_codes &= (
                                testing_criterion.complement_possible_codes
                            )
                            testing_options.remove(testing_criterion)
                            self.steps.append(f"""\
{testing_card} option {testing_criterion} ruled out due to superfluity.
It would make {other_card} superfluous.
There are now {len(self.possible_codes)} possbile codes.""")

    def uniqueness(self):
        valid: list[tuple[list[Criterion], Code]] = []
        for criterion_options in itertools.product(
            *self.card_criterion_options
        ):
            possible_codes = self.possible_codes.copy()
            for criterion in criterion_options:
                possible_codes &= criterion.possible_codes

            if len(possible_codes) == 1:
                valid.append((list(criterion_options), possible_codes.pop()))

        for i, criterion_options in enumerate(self.card_criterion_options):
            for criterion in criterion_options:
                if all(
                    criterion not in possible_criteria
                    for possible_criteria, _ in valid
                ):
                    card = self.criteria_cards[i]
                    self.possible_codes &= criterion.complement_possible_codes
                    criterion_options.remove(criterion)
                    self.steps.append(f"""\
{card} option {criterion} ruled out due to uniqueness.
No possible other criteria would give exactly 1 solution.
There are now {len(self.possible_codes)} possbile codes.""")

        self.possible_codes &= set(code for _, code in valid)
