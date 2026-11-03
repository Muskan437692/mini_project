"""Basic mathematical operations with strict validation and error handling."""

import math
from typing import Union

from calculator.exceptions import (
    DivisionByZeroError,
    InvalidInputError,
    NegativeSquareRootError,
)

Number = Union[int, float]


def _ensure_number(val: Number, name: str = "operand") -> Number:
    """Validate that the given value is a real number (int or float)."""
    if isinstance(val, bool) or not isinstance(val, (int, float)):
        raise InvalidInputError(f"Expected numeric {name}, got {type(val).__name__}: {val!r}")
    if math.isnan(val) or math.isinf(val):
        raise InvalidInputError(f"Invalid non-finite number for {name}: {val}")
    return val


def add(a: Number, b: Number) -> Number:
    """Return the sum of a and b."""
    _ensure_number(a, "first operand")
    _ensure_number(b, "second operand")
    return a + b


def subtract(a: Number, b: Number) -> Number:
    """Return the difference of a and b (a - b)."""
    _ensure_number(a, "first operand")
    _ensure_number(b, "second operand")
    return a - b


def multiply(a: Number, b: Number) -> Number:
    """Return the product of a and b."""
    _ensure_number(a, "first operand")
    _ensure_number(b, "second operand")
    return a * b


def divide(a: Number, b: Number) -> float:
    """Return the quotient of a divided by b.

    Raises:
        DivisionByZeroError: If b is zero.
    """
    _ensure_number(a, "first operand")
    _ensure_number(b, "second operand")
    if b == 0:
        raise DivisionByZeroError("Cannot divide by zero.")
    return a / b


def modulo(a: Number, b: Number) -> Number:
    """Return the remainder of a divided by b (a % b).

    Raises:
        DivisionByZeroError: If b is zero.
    """
    _ensure_number(a, "first operand")
    _ensure_number(b, "second operand")
    if b == 0:
        raise DivisionByZeroError("Cannot perform modulo by zero.")
    return a % b


def power(base: Number, exponent: Number) -> Number:
    """Return base raised to the power of exponent.

    Raises:
        InvalidInputError: If calculation results in complex number or overflow.
    """
    _ensure_number(base, "base")
    _ensure_number(exponent, "exponent")
    if base < 0 and not isinstance(exponent, int) and not exponent.is_integer():
        raise InvalidInputError("Negative base with non-integer exponent results in a complex number.")
    try:
        result = base ** exponent
    except OverflowError as err:
        raise InvalidInputError("Result exceeded maximum allowable number size (overflow).") from err
    return result


def square_root(a: Number) -> float:
    """Return the square root of a.

    Raises:
        NegativeSquareRootError: If a is negative.
    """
    _ensure_number(a, "operand")
    if a < 0:
        raise NegativeSquareRootError("Cannot compute square root of a negative number in real domain.")
    return math.sqrt(a)
