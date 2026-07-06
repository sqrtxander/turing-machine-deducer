from typing import Callable


class Code:
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
