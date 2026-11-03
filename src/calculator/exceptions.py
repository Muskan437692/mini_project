"""Custom exception hierarchy for the calculator application."""


class CalculatorError(Exception):
    """Base exception class for all calculator-related errors."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when division or modulo by zero is attempted."""
    pass


class NegativeSquareRootError(CalculatorError):
    """Raised when square root of a negative number is attempted."""
    pass


class InvalidInputError(CalculatorError):
    """Raised when operands or expressions are malformed or invalid."""
    pass
