from typing import Callable, override

from .code import Code, all_codes


class Criterion:
    @override
    def __init__(
        self, card_id: int, _checks: list[Callable[[Code], bool]]
    ) -> None:
        self.card_id = card_id
        self._checks: list[Callable[[Code], bool]] = _checks
        self.possible_codes: list[set[int]] = [
            {code for code in all_codes() if check(code)}
            for check in self._checks
        ]
        self.complement_possible_codes: list[set[int]] = [
            {
                code
                for code in all_codes()
                if any(
                    check(code)
                    for i, check in enumerate(self._checks)
                    if i != curr
                )
            }
            for curr in range(len(self._checks))
        ]

    @property
    def num_options(self) -> int:
        return len(self._checks)

    def is_valid_code(self, code: Code, option: int) -> bool:
        if option < 0 or option >= self.num_options:
            raise ValueError(
                f"Option must be an int in the range [0, {self.num_options})"
            )

        return self._checks[option](code)

    @override
    def __str__(self) -> str:
        return f"Criteria card #{self.card_id}"

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Criterion):
            return False

        return self.card_id == other.card_id
