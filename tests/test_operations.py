"""Unit tests for individual calculator operations."""

import unittest
from calculator.exceptions import (
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


class TestCalculatorOperations(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-5, 5), 0)
        self.assertAlmostEqual(add(0.1, 0.2), 0.3, places=7)

    def test_subtraction(self):
        self.assertEqual(subtract(10, 4), 6)
        self.assertEqual(subtract(4, 10), -6)
        self.assertAlmostEqual(subtract(5.5, 2.2), 3.3)

    def test_multiplication(self):
        self.assertEqual(multiply(3, 7), 21)
        self.assertEqual(multiply(-2, 5), -10)
        self.assertEqual(multiply(0, 100), 0)
        self.assertAlmostEqual(multiply(2.5, 4), 10.0)

    def test_division(self):
        self.assertEqual(divide(10, 2), 5.0)
        self.assertAlmostEqual(divide(1, 3), 0.33333333)

    def test_division_by_zero(self):
        with self.assertRaises(DivisionByZeroError):
            divide(5, 0)

    def test_modulo(self):
        self.assertEqual(modulo(10, 3), 1)
        self.assertEqual(modulo(15, 5), 0)

    def test_modulo_by_zero(self):
        with self.assertRaises(DivisionByZeroError):
            modulo(10, 0)

    def test_power(self):
        self.assertEqual(power(2, 3), 8)
        self.assertEqual(power(9, 0.5), 3.0)
        self.assertEqual(power(5, 0), 1)

    def test_power_negative_fractional_raises(self):
        with self.assertRaises(InvalidInputError):
            power(-4, 0.5)

    def test_square_root(self):
        self.assertEqual(square_root(16), 4.0)
        self.assertEqual(square_root(0), 0.0)
        self.assertAlmostEqual(square_root(2), 1.41421356, places=7)

    def test_square_root_negative_raises(self):
        with self.assertRaises(NegativeSquareRootError):
            square_root(-1)

    def test_invalid_types(self):
        with self.assertRaises(InvalidInputError):
            add("3", 4)  # type: ignore
        with self.assertRaises(InvalidInputError):
            add(True, 4)  # Booleans rejected
        with self.assertRaises(InvalidInputError):
            subtract(None, 4)  # type: ignore
        with self.assertRaises(InvalidInputError):
            add(float("nan"), 1)
        with self.assertRaises(InvalidInputError):
            add(float("inf"), 1)


if __name__ == "__main__":
    unittest.main()
