import itertools
from typing import Callable, override

from .code import Code, all_codes
from .criterion import Criterion, PrunableCriteriaCard, format_criteria


class Deducer:
    @override
    def __init__(self, criteria_cards: list[PrunableCriteriaCard]) -> None:
        self.criteria_cards: list[PrunableCriteriaCard] = criteria_cards
        self.possible_codes: set[Code] = set(all_codes())
        self.steps: list[str] = []

    def print_steps(self) -> None:
        print("\n\n".join(self.steps))

    def _deduce_with(
        self, f: Callable[[PrunableCriteriaCard, Criterion], bool]
    ) -> bool:
        deduced = False
        for testing_card in self.criteria_cards:
            if len(testing_card.possible_criteria) == 1:
                continue
            for testing_criterion in testing_card.criteria:
                if testing_criterion not in testing_card.possible_criteria:
                    continue
                if f(testing_card, testing_criterion):
                    deduced = True
                    if len(testing_card.possible_criteria) == 1:
                        correct_criterion = testing_card.possible_criteria[0]
                        self.possible_codes &= correct_criterion.possible_codes
                        self.steps.append(f"""\
{testing_card} has only one remaining criterion.
Therefore {testing_card}__{correct_criterion} is true.""")
        return deduced

    def deduce(self) -> None:
        def superfluity(n: int):
            return lambda a, b: self.superfluity_n(a, b, n)

        self.steps.append(
            "\n".join(
                card.format_possible_criteria() for card in self.criteria_cards
            )
        )

        for n in range(1, len(self.criteria_cards)):
            self.steps.append(f"=== Superfluity ({n}) ===")
            deduced = True
            while deduced:
                deduced = deduced and self._deduce_with(superfluity(n))

            self.steps.append(
                "\n".join(
                    card.format_possible_criteria()
                    for card in self.criteria_cards
                )
            )
        self.steps.append("=== Uniqueness ===")
        self._deduce_with(self.uniqueness)

    def superfluity_n(
        self,
        testing_card: PrunableCriteriaCard,
        testing_criterion: Criterion,
        n: int,
    ) -> bool:
        if len(self.criteria_cards) < n - 1:
            return False

        if testing_criterion not in testing_card.possible_criteria:
            return False

        other_cards = [
            card for card in self.criteria_cards if card is not testing_card
        ]

        for testing_cards in itertools.combinations(other_cards, n - 1):
            testing_possible_codes = _testing_possible_codes(
                testing_criterion, testing_cards
            )

            for other_card in other_cards:
                if other_card in testing_cards:
                    continue

                other_criterion = _find_superfluous_criterion(
                    other_card, testing_possible_codes
                )

                if other_criterion is None:
                    continue

                self._apply_superfluity(
                    testing_card,
                    testing_criterion,
                    other_card,
                    other_criterion,
                    testing_cards,
                )

                return True

        return False

    def _apply_superfluity(
        self,
        testing_card: PrunableCriteriaCard,
        testing_criterion: Criterion,
        other_card: PrunableCriteriaCard,
        other_criterion: Criterion,
        testing_cards: tuple[PrunableCriteriaCard, ...],
    ) -> None:
        self.possible_codes &= testing_criterion.other_possible_codes
        testing_card.prune(testing_criterion)
        clause = ""
        if testing_cards:
            conditions = [
                format_criteria(card.possible_criteria)
                for card in testing_cards
            ]
            clause = f"Since {' AND '.join(conditions)} is known true,"
        excluding = format_criteria(
            criterion
            for criterion in other_card.criteria
            if criterion is not other_criterion
        )
        lines = [
            f"Considering {testing_card}__{testing_criterion} "
            f"and {other_card}.",
            f"    {clause}" if clause else None,
            f"    {testing_criterion} is contained by {other_criterion},",
            f"    {testing_criterion} is disjoint to {excluding}.",
            f"        => {other_card} is superfluous.",
            f"    Therefore {testing_card}__{testing_criterion} is ruled out.",
        ]
        self.steps.append("\n".join(line for line in lines if line is not None))

    def uniqueness(
        self, testing_card: PrunableCriteriaCard, testing_criterion: Criterion
    ) -> bool:
        if testing_criterion not in testing_card.possible_criteria:
            return False
        unique = 0
        for criterion_options in itertools.product(
            *[
                [testing_criterion]
                if card is testing_card
                else card.possible_criteria
                for card in self.criteria_cards
            ]
        ):
            possible_codes = set.intersection(
                self.possible_codes.copy(),
                *[criterion.possible_codes for criterion in criterion_options],
            )

            if len(possible_codes) == 1:
                if unique == 1:
                    return False
                unique += 1

        if unique == 1:
            return False

        self.possible_codes &= testing_criterion.other_possible_codes
        testing_card.prune(testing_criterion)
        self.steps.append(f"""\
{testing_card}__{testing_criterion} true
    => Solution is any of ...
""")
        return True


def _testing_possible_codes(
    testing_criterion: Criterion,
    testing_cards: tuple[PrunableCriteriaCard, ...],
) -> set[Code]:
    card_possible_codes = [
        set.union(
            *(criteria.possible_codes for criteria in card.possible_criteria)
        )
        for card in testing_cards
    ]
    return testing_criterion.possible_codes.intersection(*card_possible_codes)


def _find_superfluous_criterion(
    other_card: PrunableCriteriaCard,
    testing_possible_codes: set[Code],
) -> Criterion | None:
    for other_criterion in other_card.criteria:
        contained = testing_possible_codes.issubset(
            other_criterion.possible_codes
        )
        disjoint = not testing_possible_codes.intersection(
            other_criterion.other_possible_codes
        )
        if disjoint and contained:
            return other_criterion
    return None
