import json
from contextlib import contextmanager
from typing import override

from .criterion import CriteriaCard, Criterion

type NestedStr = str | list[NestedStr]


class DeductionLog:
    @override
    def __init__(self) -> None:
        self._step: list[list[NestedStr]] = [[]]
        self._stack: list[NestedStr] = []

    def add(self, lines: list[str]) -> None:
        self._step[-1].append(lines)

    def write(self) -> None:
        for step in self._step:
            self._stack.extend(step)
        self._step = [[]]

    def wipe(self) -> None:
        self._step = [[]]

    @contextmanager
    def assuming(self, card: CriteriaCard, criterion: Criterion):
        block: list[NestedStr] = [f"BEGIN ASSUMING {card}__{criterion}"]
        self._step[-1].append(block)
        self._step.append(block)
        try:
            yield
        finally:
            block.append("END ASSUMING")
            self._step.pop()

    @contextmanager
    def checking(
        self,
        card: CriteriaCard,
        criterion: Criterion,
        against: CriteriaCard | None = None,
    ):
        label = f"BEGIN CHECKING {card}__{criterion}"
        if against is not None:
            label += f" against {against}"
        block: list[NestedStr] = [label]
        self._step[-1].append(block)
        self._step.append(block)
        try:
            yield
        finally:
            block.append("END CHECKING")
            self._step.pop()

    @override
    def __repr__(self) -> str:
        return json.dumps(self._stack, indent=4)

    @override
    def __str__(self) -> str:
        def _aux(steps: list[NestedStr], level: int = 0) -> None:
            for step in steps:
                if isinstance(step, list):
                    _aux(step, level + 1)
                else:
                    acc.append("    " * (level - 1) + step)

        acc = []
        _aux(self._stack)
        return "\n".join(acc)
