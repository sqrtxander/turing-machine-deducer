from typing import Callable

from .code import Code


class Criterion:
    def __init__(self, card_id, _checks) -> None:
        self.card_id = card_id
        self._checks: list[Callable[[Code], bool]] = _checks
        self.correct_option: int | None = None
        self.possible_options = set(range(self.num_options))

    @property
    def num_options(self) -> int:
        return len(self._checks)

    def is_valid_code(self, code: Code, option: int | None = None) -> bool:
        if option is None:
            option = self.correct_option

        if option is None or option < 0 or option >= self.num_options:
            raise ValueError(
                f"Option must be an int in the range [0, {self.num_options})"
            )

        return self._checks[option](code)

    def __str__(self) -> str:
        return f"Criteria card #{self.card_id}"
