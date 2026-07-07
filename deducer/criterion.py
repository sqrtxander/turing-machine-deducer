from functools import cached_property
from typing import Callable, override

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
    def complement_possible_codes(self) -> set[Code]:
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
