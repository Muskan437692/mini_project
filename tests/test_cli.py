"""Unit tests for the CLI interface."""

import io
import unittest
from unittest.mock import patch

from calculator.cli import format_number, main, repl
from calculator.engine import Calculator


class TestCLI(unittest.TestCase):
    def test_format_number(self):
        self.assertEqual(format_number(5.0), "5")
        self.assertEqual(format_number(5), "5")
        self.assertEqual(format_number(3.1415), "3.1415")

    def test_main_eval_flag(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            exit_code = main(["-e", "2 + 2 * 3"])
            self.assertEqual(exit_code, 0)
            self.assertEqual(mock_stdout.getvalue().strip(), "8")

    def test_main_positional_expr(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            exit_code = main(["10", "+", "5"])
            self.assertEqual(exit_code, 0)
            self.assertEqual(mock_stdout.getvalue().strip(), "15")

    def test_main_eval_error(self):
        with patch("sys.stderr", new_callable=io.StringIO) as mock_stderr:
            exit_code = main(["-e", "10 / 0"])
            self.assertEqual(exit_code, 1)
            self.assertIn("Cannot divide by zero", mock_stderr.getvalue())

    def test_repl_session(self):
        inputs = iter([
            "add 5",
            "mul 3",
            "ms",
            "clear",
            "mr",
            "sqrt",
            "history",
            "help",
            "quit",
        ])
        with patch("builtins.input", lambda _: next(inputs)), \
             patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            calc = Calculator(10)
            repl(calc)
            out = mock_stdout.getvalue()
            self.assertIn("= 15", out)
            self.assertIn("= 45", out)
            self.assertIn("Memory Stored: 45", out)
            self.assertIn("= 0", out)
            self.assertIn("= 45", out)
            self.assertIn("No calculations in history" if not calc.history else "history", out)
            self.assertIn("Goodbye!", out)


if __name__ == "__main__":
    unittest.main()
