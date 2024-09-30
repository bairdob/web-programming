import math
from fractions import Fraction


def numbers_factory_method(x: float | str, y: float | str) -> tuple[float, float]:
    if isinstance(x, float) and isinstance(y, float):
        return x, y
    elif isinstance(x, str) and isinstance(y, str):
        try:
            x = Fraction(x)
            y = Fraction(y)
        except ValueError:
            raise
        else:
            return float(x), float(y)

    raise TypeError("Both arguments must be either float or str")


class Calculator:

    @staticmethod
    def add(x: float | str, y: float | str) -> float:
        x, y = numbers_factory_method(x, y)
        return float(x + y)

    @staticmethod
    def subtract(x: float | str, y: float | str) -> float:
        x, y = numbers_factory_method(x, y)
        return float(x - y)

    @staticmethod
    def multiply(x: float | str, y: float | str) -> float:
        x, y = numbers_factory_method(x, y)
        return float(x * y)

    @staticmethod
    def divide(x: float | str, y: float | str) -> float:
        x, y = numbers_factory_method(x, y)
        return float(x / y)

    @staticmethod
    def sqrt(x: float) -> float:
        return math.sqrt(x)

    @staticmethod
    def round(number: float, digit: int) -> float:
        return round(number, digit)

    @staticmethod
    def pow(base: float, exp: int) -> float:
        return pow(base, exp)
