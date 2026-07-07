from typing import Callable, Self, override


class Code:
    @override
    def __init__(self, triangle: int, square: int, circle: int) -> None:
        if triangle <= 0 or triangle > 5:
            raise ValueError(
                f"Expected code digits in the range [1, 5]. Got {triangle=}"
            )

        if square <= 0 or square > 5:
            raise ValueError(
                f"Expected code digits in the range [1, 5]. Got {square=}"
            )

        if circle <= 0 or circle > 5:
            raise ValueError(
                f"Expected code digits in the range [1, 5]. Got {circle=}"
            )

        self.triangle = triangle
        self.square = square
        self.circle = circle

        self._lst = [triangle, square, circle]

        self.set = set(self._lst)

    def sum(self) -> int:
        return sum(self._lst)

    def count(self, value: int) -> int:
        return sum(digit == value for digit in self._lst)

    def count_where(self, pred: Callable[[int], bool]) -> int:
        return sum(pred(digit) for digit in self._lst)

    def count_even(self) -> int:
        return self.count_where(lambda d: d % 2 == 0)

    def count_odd(self) -> int:
        return self.count_where(lambda d: d % 2 != 0)

    @override
    def __str__(self) -> str:
        return f"{self.triangle}{self.square}{self.circle}"

    def __lt__(self, other: Self) -> bool:
        return (self.triangle, self.square, self.circle) < (
            other.triangle,
            other.square,
            other.circle,
        )

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Code):
            return False

        return (self.triangle, self.square, self.circle) == (
            other.triangle,
            other.square,
            other.circle,
        )

    def __hash__(self):
        return hash((self.triangle, self.square, self.circle))


def all_codes():
    return [
        Code(triangle, square, circle)
        for triangle in range(1, 6)
        for square in range(1, 6)
        for circle in range(1, 6)
    ]
