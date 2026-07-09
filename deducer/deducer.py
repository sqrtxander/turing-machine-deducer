import itertools
from types import GeneratorType
from typing import Callable, override

from .code import Code, all_codes
from .criterion import Criterion, PrunableCriteriaCard, format_criteria
from .deduction_log import DeductionLog
from .errors import UnsolvableError


class Deducer:
    @override
    def __init__(self, criteria_cards: list[PrunableCriteriaCard]) -> None:
        self.criteria_cards: list[PrunableCriteriaCard] = criteria_cards
        self.possible_codes: set[Code] = set(all_codes())
        self.deduction_log = DeductionLog()
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
        self.deduction_log.add(
            [
                f"{card} has only one remaining criterion.",
                f"Therefore {card}__{correct_criterion} is true.",
            ]
        )

    def print_steps(self) -> None:
        print(self.deduction_log)

    def _log_criteria_options(self) -> None:
        self.deduction_log.add(
            [card.format_possible_criteria() for card in self.criteria_cards]
        )
        self.deduction_log.write()

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

        self.possible_codes = self._recalculate_possible_codes()

    def apply_assumption(self) -> None:
        for card in self.criteria_cards:
            card.apply_assumption()

    def next_assumption(self) -> bool:
        result = True
        for _ in range(2):
            for card, criterion in self._assumption_gen:
                if len(card.assumed_possible_criteria) == 1:
                    continue
                if criterion not in card.assumed_possible_criteria:
                    continue
                self._assumed_card, self._assumed_criterion = card, criterion
                self._assumed_card.assume(self._assumed_criterion)
                self.possible_codes &= self._assumed_criterion.possible_codes
                return result
            self._assumption_gen = self._make_assumption_gen()
            result = False
        return result

    def _deduce_with(
        self, f: Callable[[PrunableCriteriaCard, Criterion], bool]
    ) -> bool:
        for testing_card in self.criteria_cards:
            if (
                self._assumed_criterion is None
                and len(testing_card.assumed_possible_criteria) == 1
            ):
                continue
            for testing_criterion in testing_card.criteria:
                if (
                    testing_criterion
                    not in testing_card.assumed_possible_criteria
                ):
                    continue
                if f(testing_card, testing_criterion):
                    if not testing_card.assumed_possible_criteria:
                        if self._assumed_card is None:
                            self.deduction_log.add(
                                [
                                    f"{testing_card} has no possible criteria, "
                                    "and we are not in an assumption.",
                                    "Therefore the verifiers provided are "
                                    "incompatible with one another.",
                                    "There is no valid solution.",
                                ]
                            )

                            return True

                        self.deduction_log.add(
                            [
                                f"{testing_card} has no possible criteria.",
                                "Therefore our assumption was wrong, and "
                                f"{self._assumed_card}__"
                                f"{self._assumed_criterion} is ruled out.",
                            ]
                        )

                        return True
                    if self._assumed_card is None:
                        self._if_one_remaining_criterion(testing_card)
        return False

    def _superfluity(
        self, n: int
    ) -> Callable[[PrunableCriteriaCard, Criterion], bool]:
        return lambda a, b: self.superfluity_n(a, b, n)

    def _deduce_aux(self) -> bool:
        contra = False

        for n in range(1, len(self.criteria_cards)):
            contra = self._deduce_with(self._superfluity(n))
            if contra:
                break

        if contra and self._assumed_card is None:
            self.deduction_log.write()
            raise UnsolvableError

        if not contra:
            contra = self._deduce_with(self.uniqueness)

        if self._assumed_card is None:
            self.apply_assumption()

        self.restore_from_assumption(contra)
        return self._assumed_card is None or contra

    def deduce(self) -> bool:
        self._log_criteria_options()

        self._deduce_aux()
        self.deduction_log.write()

        self._log_criteria_options()

        made_progress = False
        while not self.is_solved():
            if not self.next_assumption():
                if not made_progress:
                    break
                made_progress = False
            if self._assumed_card is None or self._assumed_criterion is None:
                break
            with self.deduction_log.assuming(
                self._assumed_card, self._assumed_criterion
            ):
                contra = self._deduce_aux()
            if contra:
                made_progress = True
                self.deduction_log.write()
                self._if_one_remaining_criterion(self._assumed_card)
                self.deduction_log.write()
                self._log_criteria_options()
            else:
                self.deduction_log.wipe()

        if not self.is_solved():
            self.deduction_log.add(["I could not deduce all criteria cards."])
            self.deduction_log.write()
            return False

        self.deduction_log.add(
            [
                "All criteria cards deduced.",
                f"The code is {self.possible_codes.pop()}.",
            ]
        )
        self.deduction_log.write()
        return True

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

        lines: list[str] = [
            f"{testing_criterion} is contained by {other_criterion},"
            if criterion is other_criterion
            else f"{testing_criterion} is disjoint from {criterion},"
            for criterion in other_card.criteria
        ]
        if lines:
            lines[-1] = f"{lines[-1].removesuffix(',')}."
        with self.deduction_log.checking(
            testing_card, testing_criterion, other_card
        ):
            self.deduction_log.add(
                [
                    line
                    for line in [
                        f"{clause}" if clause else None,
                        *lines,
                        f"=> {other_card} is superfluous.",
                        f"Therefore {testing_card}__{testing_criterion} "
                        "is ruled out.",
                    ]
                    if line is not None
                ]
            )

    def uniqueness(
        self, testing_card: PrunableCriteriaCard, testing_criterion: Criterion
    ) -> bool:
        all_codes = {}
        for criterion_options in itertools.product(
            *[
                [testing_criterion]
                if card is testing_card
                else card.assumed_possible_criteria
                for card in self.criteria_cards
            ]
        ):
            possible_codes = self.possible_codes.intersection(
                *[criterion.possible_codes for criterion in criterion_options],
            )

            all_codes[criterion_options] = possible_codes

        if not any(
            len(possible_codes) == 1 for possible_codes in all_codes.values()
        ):
            self._apply_uniqueness(testing_card, testing_criterion, all_codes)
            return True

        return False

    def _apply_uniqueness(
        self,
        testing_card: PrunableCriteriaCard,
        testing_criterion: Criterion,
        all_codes: dict[tuple[Criterion, ...], set[Code]],
    ) -> None:
        option_mask = [
            len(card.assumed_possible_criteria) > 1
            for card in self.criteria_cards
        ]

        def _format_line(
            criteria: tuple[Criterion, ...], codes: set[Code]
        ) -> str:
            filtered_criteria = itertools.compress(criteria, option_mask)
            criteria_s = ", ".join(
                [str(criterion) for criterion in filtered_criteria]
            )
            codes_s = ", ".join(str(code) for code in sorted(list(codes)))
            if criteria_s:
                return f"{criteria_s} gives possible codes {{{codes_s}}},"
            else:
                return f"Possible codes {codes_s},"

        self.possible_codes &= testing_criterion.other_possible_codes
        testing_card.prune(testing_criterion)

        lines: list[str] = [
            _format_line(criteria, codes)
            for criteria, codes in all_codes.items()
        ]
        if lines:
            lines[-1] = f"{lines[-1].removesuffix(',')}."
        with self.deduction_log.checking(testing_card, testing_criterion):
            self.deduction_log.add(
                [
                    *lines,
                    "=> No possible unique code.",
                    f"Therefore {testing_card}__{testing_criterion} "
                    "is ruled out.",
                ]
            )


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
