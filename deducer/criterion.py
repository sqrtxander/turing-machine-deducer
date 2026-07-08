from functools import cached_property
from typing import Callable, Iterable, override

from .code import Code, all_codes


class CriteriaCard:
    @override
    def __init__(
        self, _id: str, _checks: dict[str, Callable[[Code], bool]]
    ) -> None:
        self._id: str = _id
        self.criteria: list[Criterion] = [
            Criterion(self, criterion_id, check)
            for criterion_id, check in _checks.items()
        ]

    @property
    def num_options(self) -> int:
        return len(self.criteria)

    @override
    def __repr__(self) -> str:
        return self._id

    @override
    def __format__(self, fmt: str) -> str:
        return f"{repr(self):{fmt}}"

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CriteriaCard):
            return False

        return self._id == other._id


class Criterion:
    @override
    def __init__(
        self,
        _card: CriteriaCard,
        _criterion_id: str,
        check: Callable[[Code], bool],
    ) -> None:
        self._card = _card
        self._criterion_id: str = _criterion_id
        self.check: Callable[[Code], bool] = check
        self.possible_codes: set[Code] = {
            code for code in all_codes() if self.check(code)
        }

    @cached_property
    def other_possible_codes(self) -> set[Code]:
        return set().union(
            *(
                other.possible_codes
                for other in self._card.criteria
                if other is not self
            )
        )

    @override
    def __repr__(self) -> str:
        return self._criterion_id


class PrunableCriteriaCard(CriteriaCard):
    @override
    def __init__(self, source: CriteriaCard) -> None:
        self._id: str = source._id
        self.criteria: list[Criterion] = source.criteria
        self.possible_criteria: list[Criterion] = source.criteria.copy()

    def prune(self, criterion: Criterion) -> None:
        self.possible_criteria.remove(criterion)

    def format_possible_criteria(self) -> str:
        return f"{str(self)[:3]} [ {
            ' | '.join(str(criteria) for criteria in self.possible_criteria)
        } ]"


def format_criteria(criteria: Iterable[Criterion]) -> str:
    criteria_strs = [str(criterion) for criterion in criteria]
    s = " OR ".join(criteria_strs)
    if len(criteria_strs) == 1:
        return s
    return f"({s})"
