"""A well-structured, modular calculator library and CLI."""

from calculator.engine import Calculator, evaluate
from calculator.exceptions import (
    CalculatorError,
    DivisionByZeroError,
    InvalidInputError,
    NegativeSquareRootError,
)
from calculator.operations import (
    add,
    divide,
    modulo,
    multiply,
    power,
    square_root,
    subtract,
)

__all__ = [
    "Calculator",
    "evaluate",
    "CalculatorError",
    "DivisionByZeroError",
    "NegativeSquareRootError",
    "InvalidInputError",
    "add",
    "subtract",
    "multiply",
    "divide",
    "power",
    "modulo",
    "square_root",
]
