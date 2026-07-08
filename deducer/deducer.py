import functools
import itertools
from typing import override

from .code import Code, all_codes
from .criterion import Criterion, PrunableCriteriaCard


class Deducer:
    @override
    def __init__(self, criteria_cards: list[PrunableCriteriaCard]) -> None:
        self.criteria_cards: list[PrunableCriteriaCard] = criteria_cards
        self.possible_codes: set[Code] = set(all_codes())
        self.steps: list[str] = []

    def print_steps(self) -> None:
        print("\n\n".join(self.steps))

    def deduce(self) -> None:
        self.steps.append("=== Superfluity (1) ===")
        self.superfluity()
        self.steps.append(
            "\n".join(
                [
                    " | ".join(str(crit) for crit in card.possible_criteria)
                    for card in self.criteria_cards
                ]
            )
        )
        self.steps.append("=== Superfluity (2) ===")
        self.superfluity_n(2)
        self.steps.append(
            "\n".join(
                [
                    " | ".join(str(crit) for crit in card.possible_criteria)
                    for card in self.criteria_cards
                ]
            )
        )
        self.steps.append("=== Uniqueness ===")
        self.uniqueness()
        self.steps.append(
            "\n".join(
                [
                    " | ".join(str(crit) for crit in card.possible_criteria)
                    for card in self.criteria_cards
                ]
            )
        )

    def superfluity(self) -> None:
        for testing_card in self.criteria_cards:
            for other_card in self.criteria_cards:
                if testing_card is other_card:
                    continue
                for testing_criterion in testing_card.criteria:
                    if testing_criterion not in testing_card.possible_criteria:
                        continue
                    for other_criterion in other_card.criteria:
                        if (
                            not testing_criterion.possible_codes.intersection(
                                other_criterion.complement_possible_codes
                            )
                        ) and testing_criterion.possible_codes.issubset(
                            other_criterion.possible_codes
                        ):
                            self.possible_codes &= (
                                testing_criterion.complement_possible_codes
                            )
                            testing_card.prune(testing_criterion)
                            self.steps.append(f"""\
If {testing_card} option {testing_criterion} were true, it would make \
{other_card} superfluous.
Therefore {testing_card} option {testing_criterion} is ruled out.
There are now {len(self.possible_codes)} possible codes.""")
                            break

    def superfluity_n(self, n: int) -> None:
        solved_cards = [
            card
            for card in self.criteria_cards
            if len(card.possible_criteria) == 1
        ]
        unsolved_cards = [
            card
            for card in self.criteria_cards
            if len(card.possible_criteria) != 1
        ]
        for testing_card, known_cards in itertools.product(
            unsolved_cards, itertools.combinations(solved_cards, n - 1)
        ):
            testing_cards = [testing_card, *known_cards]
            for other_card in self.criteria_cards:
                if any(other_card is card for card in testing_cards):
                    continue
                for testing_criteria in itertools.product(
                    *[card.possible_criteria for card in testing_cards]
                ):
                    testing_possible_codes = functools.reduce(
                        set.intersection,
                        (option.possible_codes for option in testing_criteria),
                    )
                    for other_criterion in other_card.criteria:
                        if all(
                            other_criterion is not criterion
                            for criterion in other_card.criteria
                        ):
                            break
                        if (
                            not testing_possible_codes.intersection(
                                other_criterion.complement_possible_codes
                            )
                        ) and testing_possible_codes.issubset(
                            other_criterion.possible_codes
                        ):
                            testing_criterion = testing_criteria[0]
                            self.possible_codes &= (
                                testing_criterion.complement_possible_codes
                            )
                            testing_card.prune(testing_criterion)
                            self.steps.append(f"""\
If {testing_card} option {testing_criterion} were true, because of \
{" and ".join(str(c) for c in known_cards)}, {other_card} would be superfluous.
Therefore {testing_card} option {testing_criterion} is ruled out.
There are now {len(self.possible_codes)} possible codes.""")
                            break

    def uniqueness(self) -> None:
        valid: list[tuple[list[Criterion], Code]] = []
        for criterion_options in itertools.product(
            *[card.possible_criteria for card in self.criteria_cards]
        ):
            possible_codes = self.possible_codes.copy()
            for criterion in criterion_options:
                possible_codes &= criterion.possible_codes

            if len(possible_codes) == 1:
                valid.append((list(criterion_options), possible_codes.pop()))

        for v, c in valid:
            self.steps.append(f"""\
{c}
{"\n".join(str(crit) for crit in v)}""")

        for i, criterion_options in enumerate(
            card.possible_criteria for card in self.criteria_cards
        ):
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
There are now {len(self.possible_codes)} possbile codes.
{self.possible_codes}""")

        self.possible_codes &= set(code for _, code in valid)
