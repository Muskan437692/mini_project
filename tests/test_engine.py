"""Unit tests for the Calculator class and safe expression evaluator."""

import unittest
from calculator.engine import Calculator, evaluate
from calculator.exceptions import (
    DivisionByZeroError,
    InvalidInputError,
    NegativeSquareRootError,
)


class TestCalculatorClass(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator(10)

    def test_initial_state(self):
        self.assertEqual(self.calc.current_value, 10)
        self.assertEqual(self.calc.memory, 0)
        self.assertEqual(len(self.calc.history), 0)

    def test_chained_arithmetic(self):
        self.calc.add(5)
        self.assertEqual(self.calc.current_value, 15)
        self.calc.subtract(3)
        self.assertEqual(self.calc.current_value, 12)
        self.calc.multiply(2)
        self.assertEqual(self.calc.current_value, 24)
        self.calc.divide(4)
        self.assertEqual(self.calc.current_value, 6.0)
        self.calc.modulo(4)
        self.assertEqual(self.calc.current_value, 2.0)
        self.calc.power(3)
        self.assertEqual(self.calc.current_value, 8.0)
        self.calc.square_root()
        self.assertAlmostEqual(self.calc.current_value, 2.82842712)

    def test_history_and_clear(self):
        self.calc.add(2)
        self.calc.multiply(3)
        self.assertEqual(len(self.calc.history), 2)
        self.assertEqual(self.calc.history[0].result, 12)
        self.assertEqual(self.calc.history[1].result, 36)
        self.calc.clear_history()
        self.assertEqual(len(self.calc.history), 0)

    def test_memory_operations(self):
        self.calc.memory_store(50)
        self.assertEqual(self.calc.memory, 50)
        self.calc.memory_add(10)
        self.assertEqual(self.calc.memory, 60)
        self.calc.memory_subtract(20)
        self.assertEqual(self.calc.memory, 40)
        self.calc.memory_recall()
        self.assertEqual(self.calc.current_value, 40)
        self.calc.memory_clear()
        self.assertEqual(self.calc.memory, 0)

    def test_reset(self):
        self.calc.add(10)
        self.calc.reset(0)
        self.assertEqual(self.calc.current_value, 0)

    def test_evaluate_expression_method(self):
        res = self.calc.evaluate_expression("10 * 3 + 2")
        self.assertEqual(res, 32)
        self.assertEqual(self.calc.current_value, 32)


class TestSafeExpressionEvaluator(unittest.TestCase):
    def test_basic_arithmetic(self):
        self.assertEqual(evaluate("1 + 2"), 3)
        self.assertEqual(evaluate("10 - 4"), 6)
        self.assertEqual(evaluate("3 * 5"), 15)
        self.assertEqual(evaluate("8 / 2"), 4.0)
        self.assertEqual(evaluate("7 % 4"), 3)

    def test_operator_precedence(self):
        self.assertEqual(evaluate("2 + 3 * 4"), 14)
        self.assertEqual(evaluate("(2 + 3) * 4"), 20)
        self.assertEqual(evaluate("2 + 3 ^ 2"), 11)
        self.assertEqual(evaluate("2 ** 3"), 8)

    def test_unary_operators(self):
        self.assertEqual(evaluate("-5 + 10"), 5)
        self.assertEqual(evaluate("+5 + -3"), 2)
        self.assertEqual(evaluate("-(4 * 2)"), -8)

    def test_sqrt_function(self):
        self.assertEqual(evaluate("sqrt(49)"), 7.0)
        self.assertEqual(evaluate("sqrt(16) * 3"), 12.0)

    def test_division_by_zero(self):
        with self.assertRaises(DivisionByZeroError):
            evaluate("10 / 0")
        with self.assertRaises(DivisionByZeroError):
            evaluate("10 % 0")

    def test_negative_sqrt(self):
        with self.assertRaises(NegativeSquareRootError):
            evaluate("sqrt(-9)")

    def test_disallowed_syntax_and_code_injection(self):
        # Empty string
        with self.assertRaises(InvalidInputError):
            evaluate("")
        # Arbitrary function call
        with self.assertRaises(InvalidInputError):
            evaluate("__import__('os').system('ls')")
        # Variable names
        with self.assertRaises(InvalidInputError):
            evaluate("x + y")
        # List comprehension or lambda
        with self.assertRaises(InvalidInputError):
            evaluate("[x for x in range(10)]")
        # Syntax error
        with self.assertRaises(InvalidInputError):
            evaluate("2 +* 3")


if __name__ == "__main__":
    unittest.main()
