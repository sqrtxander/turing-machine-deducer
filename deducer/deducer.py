import itertools
from types import GeneratorType
from typing import Callable, override

from .code import Code, all_codes
from .criterion import Criterion, PrunableCriteriaCard, format_criteria


class Deducer:
    @override
    def __init__(self, criteria_cards: list[PrunableCriteriaCard]) -> None:
        self.criteria_cards: list[PrunableCriteriaCard] = criteria_cards
        self.possible_codes: set[Code] = set(all_codes())
        self.steps: list[str] = []
        self.current_step: list[str] = []
        self._assumed_card: PrunableCriteriaCard | None = None
        self._assumed_criterion: Criterion | None = None
        self._assumption_gen: GeneratorType[
            tuple[PrunableCriteriaCard, Criterion]
        ] = self._make_assumption_gen()

    def _make_assumption_gen(
        self,
    ) -> GeneratorType[tuple[PrunableCriteriaCard, Criterion]]:
        return (
            (card, criterion)
            for card in self.criteria_cards
            for criterion in card.possible_criteria
        )

    def _recalculate_possible_codes(self) -> set[Code]:
        card_possible_codes = [
            set.union(
                *(
                    criteria.possible_codes
                    for criteria in card.possible_criteria
                )
            )
            for card in self.criteria_cards
        ]
        return set(all_codes()).intersection(*card_possible_codes)

    def _if_one_remaining_criterion(self, card: PrunableCriteriaCard) -> None:
        if len(card.assumed_possible_criteria) != 1:
            return
        correct_criterion = card.assumed_possible_criteria[0]
        self.possible_codes &= correct_criterion.possible_codes
        self.current_step.append(f"""\
{card} has only one remaining criterion.
Therefore {card}__{correct_criterion} is true.""")

    def print_steps(self) -> None:
        print("\n\n".join(self.steps))

    def is_solved(self) -> bool:
        return all(
            len(card.possible_criteria) == 1 for card in self.criteria_cards
        )

    def restore_from_assumption(self, contra: bool) -> None:
        for card in self.criteria_cards:
            card.unassume()

        if (
            contra
            and self._assumed_card is not None
            and self._assumed_criterion is not None
        ):
            self._assumed_card.prune(self._assumed_criterion)
            self._assumed_card.apply_assumption()
            self._if_one_remaining_criterion(self._assumed_card)

        self.possible_codes = self._recalculate_possible_codes()

    def apply_assumption(self) -> None:
        for card in self.criteria_cards:
            card.apply_assumption()

    def next_assumption(self) -> bool:
        for _ in range(2):
            for card, criterion in self._assumption_gen:
                if len(card.assumed_possible_criteria) == 1:
                    continue
                if criterion not in card.assumed_possible_criteria:
                    continue
                self._assumed_card, self._assumed_criterion = card, criterion
                self._assumed_card.assume(self._assumed_criterion)
                self.possible_codes &= self._assumed_criterion.possible_codes
                self.current_step.append(
                    f"ASSUMING {self._assumed_card}__{self._assumed_criterion}"
                )
                return True
            self._assumption_gen = self._make_assumption_gen()
        return False

    def _deduce_with(
        self, f: Callable[[PrunableCriteriaCard, Criterion], bool]
    ) -> bool:
        for testing_card in self.criteria_cards:
            for testing_criterion in testing_card.criteria:
                if (
                    testing_criterion
                    not in testing_card.assumed_possible_criteria
                ):
                    continue
                if f(testing_card, testing_criterion):
                    if len(testing_card.assumed_possible_criteria) == 0:
                        self.current_step.append(f"""\
{testing_card} has no possible criteria.
Therefore our assumption was wrong, and \
{self._assumed_card}__{self._assumed_criterion} is ruled out.""")

                        return True
                    if self._assumed_card is None:
                        self._if_one_remaining_criterion(testing_card)
        return False

    def deduce(self) -> None:
        def superfluity(n: int):
            return lambda a, b: self.superfluity_n(a, b, n)

        contra = False

        for n in range(1, len(self.criteria_cards)):
            contra = self._deduce_with(superfluity(n))
            if contra:
                break

        if not contra:
            contra = self.uniqueness()
            if contra:
                self.current_step.append("CONTRA FROM UNIQUENESS")

        if self._assumed_card is None:
            self.apply_assumption()

        self.current_step.append(
            "\n".join(
                card.format_possible_criteria() for card in self.criteria_cards
            )
        )

        self.restore_from_assumption(contra)

        if contra or self._assumed_card is None:
            self.steps.extend(self.current_step)

        self.current_step = []

        if not self.is_solved():
            self.next_assumption()
            self.deduce()
        else:
            self.steps.append(
                f"All criteria cards deduced. \
The code is {self.possible_codes.pop()}"
            )

    def superfluity_n(
        self,
        testing_card: PrunableCriteriaCard,
        testing_criterion: Criterion,
        n: int,
    ) -> bool:
        if len(self.criteria_cards) < n - 1:
            return False

        if testing_criterion not in testing_card.assumed_possible_criteria:
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
                format_criteria(card.assumed_possible_criteria)
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
        self.current_step.append(
            "\n".join(line for line in lines if line is not None)
        )

    def uniqueness(self) -> bool:
        valid = []
        for criterion_options in itertools.product(
            *[card.assumed_possible_criteria for card in self.criteria_cards]
        ):
            possible_codes = self.possible_codes.copy().intersection(
                *[criterion.possible_codes for criterion in criterion_options],
            )

            if len(possible_codes) == 1:
                valid.append(criterion_options)

        if len(valid) == 0:
            return True

        return False


def _testing_possible_codes(
    testing_criterion: Criterion,
    testing_cards: tuple[PrunableCriteriaCard, ...],
) -> set[Code]:
    card_possible_codes = [
        set.union(
            *(
                criteria.possible_codes
                for criteria in card.assumed_possible_criteria
            )
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
