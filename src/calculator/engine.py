"""Calculator Engine with safe expression parsing, state management, and history."""

import ast
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

from calculator.exceptions import (
    DivisionByZeroError,
    InvalidInputError,
    NegativeSquareRootError,
)
from calculator import operations

Number = Union[int, float]


@dataclass
class CalculationRecord:
    """Record of a past calculation."""
    expression_or_op: str
    result: Number


class Calculator:
    """Stateful calculator supporting single operations, running results, and memory."""

    def __init__(self, initial_value: Number = 0) -> None:
        operations._ensure_number(initial_value, "initial_value")
        self._current_value: Number = initial_value
        self._memory: Number = 0
        self._history: List[CalculationRecord] = []

    @property
    def current_value(self) -> Number:
        """Get the current running value of the calculator."""
        return self._current_value

    @property
    def memory(self) -> Number:
        """Get the stored memory value."""
        return self._memory

    @property
    def history(self) -> List[CalculationRecord]:
        """Get calculation history copy."""
        return list(self._history)

    def reset(self, value: Number = 0) -> Number:
        """Reset the current running value."""
        operations._ensure_number(value, "reset value")
        self._current_value = value
        return self._current_value

    def clear_history(self) -> None:
        """Clear all calculation history."""
        self._history.clear()

    # Memory functions
    def memory_store(self, value: Optional[Number] = None) -> Number:
        """Store current value or specified value into memory."""
        val_to_store = self._current_value if value is None else value
        operations._ensure_number(val_to_store, "memory store value")
        self._memory = val_to_store
        return self._memory

    def memory_recall(self) -> Number:
        """Recall stored memory value into current value."""
        self._current_value = self._memory
        return self._current_value

    def memory_add(self, value: Optional[Number] = None) -> Number:
        """Add value (or current value) to memory."""
        val = self._current_value if value is None else value
        operations._ensure_number(val, "memory add value")
        self._memory = operations.add(self._memory, val)
        return self._memory

    def memory_subtract(self, value: Optional[Number] = None) -> Number:
        """Subtract value (or current value) from memory."""
        val = self._current_value if value is None else value
        operations._ensure_number(val, "memory subtract value")
        self._memory = operations.subtract(self._memory, val)
        return self._memory

    def memory_clear(self) -> None:
        """Clear memory to zero."""
        self._memory = 0

    # Arithmetic methods updating current_value
    def add(self, value: Number) -> Number:
        """Add value to current result."""
        result = operations.add(self._current_value, value)
        self._record(f"{self._current_value} + {value}", result)
        self._current_value = result
        return result

    def subtract(self, value: Number) -> Number:
        """Subtract value from current result."""
        result = operations.subtract(self._current_value, value)
        self._record(f"{self._current_value} - {value}", result)
        self._current_value = result
        return result

    def multiply(self, value: Number) -> Number:
        """Multiply current result by value."""
        result = operations.multiply(self._current_value, value)
        self._record(f"{self._current_value} * {value}", result)
        self._current_value = result
        return result

    def divide(self, value: Number) -> Number:
        """Divide current result by value."""
        result = operations.divide(self._current_value, value)
        self._record(f"{self._current_value} / {value}", result)
        self._current_value = result
        return result

    def modulo(self, value: Number) -> Number:
        """Modulo of current result by value."""
        result = operations.modulo(self._current_value, value)
        self._record(f"{self._current_value} % {value}", result)
        self._current_value = result
        return result

    def power(self, value: Number) -> Number:
        """Raise current result to the power of value."""
        result = operations.power(self._current_value, value)
        self._record(f"{self._current_value} ^ {value}", result)
        self._current_value = result
        return result

    def square_root(self) -> Number:
        """Compute square root of current result."""
        result = operations.square_root(self._current_value)
        self._record(f"sqrt({self._current_value})", result)
        self._current_value = result
        return result

    def evaluate_expression(self, expr: str) -> Number:
        """Evaluate a mathematical expression string and update current value."""
        result = evaluate(expr)
        self._record(expr, result)
        self._current_value = result
        return result

    def _record(self, expr_str: str, result: Number) -> None:
        self._history.append(CalculationRecord(expression_or_op=expr_str, result=result))


class SafeExpressionEvaluator(ast.NodeVisitor):
    """AST-based safe evaluator for arithmetic expressions.

    Guarantees no arbitrary code execution (no function calls, attributes, imports, etc.).
    Supported: +, -, *, /, %, **, ^ (treated as power), unary +/-, numbers, parentheses, and sqrt().
    """

    SUPPORTED_BINARY_OPS = {
        ast.Add: operations.add,
        ast.Sub: operations.subtract,
        ast.Mult: operations.multiply,
        ast.Div: operations.divide,
        ast.Mod: operations.modulo,
        ast.Pow: operations.power,
        ast.BitXor: operations.power,  # Common user notation: 2 ^ 3 == 8
    }

    SUPPORTED_UNARY_OPS = {
        ast.UAdd: lambda x: operations._ensure_number(x),
        ast.USub: lambda x: operations.multiply(x, -1),
    }

    def visit(self, node: ast.AST) -> Number:
        method = getattr(self, f"visit_{type(node).__name__}", self.generic_visit)
        return method(node)

    def visit_Expression(self, node: ast.Expression) -> Number:
        return self.visit(node.body)

    def visit_Constant(self, node: ast.Constant) -> Number:
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise InvalidInputError(f"Unsupported constant type: {type(node.value).__name__}")
        return node.value

    def visit_UnaryOp(self, node: ast.UnaryOp) -> Number:
        op_type = type(node.op)
        if op_type not in self.SUPPORTED_UNARY_OPS:
            raise InvalidInputError(f"Unsupported unary operator: {op_type.__name__}")
        operand = self.visit(node.operand)
        return self.SUPPORTED_UNARY_OPS[op_type](operand)

    def visit_BinOp(self, node: ast.BinOp) -> Number:
        op_type = type(node.op)
        if op_type not in self.SUPPORTED_BINARY_OPS:
            raise InvalidInputError(f"Unsupported binary operator: {op_type.__name__}")
        left = self.visit(node.left)
        right = self.visit(node.right)
        handler = self.SUPPORTED_BINARY_OPS[op_type]
        return handler(left, right)

    def visit_Call(self, node: ast.Call) -> Number:
        # Permit only sqrt(x)
        if isinstance(node.func, ast.Name) and node.func.id == "sqrt":
            if len(node.args) != 1 or node.keywords:
                raise InvalidInputError("sqrt() takes exactly 1 argument")
            arg_val = self.visit(node.args[0])
            return operations.square_root(arg_val)
        func_name = getattr(node.func, "id", "<function>")
        raise InvalidInputError(f"Function call not permitted: {func_name}")

    def generic_visit(self, node: ast.AST) -> Number:
        raise InvalidInputError(f"Unsupported expression syntax: {type(node).__name__}")


def evaluate(expression: str) -> Number:
    """Safely parse and evaluate a math expression string.

    Examples:
        evaluate("3 + 5 * 2") -> 13
        evaluate("(10 - 2) / 4") -> 2.0
        evaluate("2 ^ 3") -> 8
        evaluate("sqrt(16) + 4") -> 8.0

    Raises:
        InvalidInputError: If syntax is invalid or unsupported.
        DivisionByZeroError: If division/modulo by zero occurs.
        NegativeSquareRootError: If square root of a negative number is evaluated.
    """
    if not isinstance(expression, str) or not expression.strip():
        raise InvalidInputError("Expression must be a non-empty string.")

    cleaned = expression.strip()
    # Normalize caret (^) to exponentiation operator (**) before AST parse so operator precedence is standard
    cleaned = cleaned.replace("^", "**")
    try:
        parsed = ast.parse(cleaned, mode="eval")
    except SyntaxError as err:
        raise InvalidInputError(f"Invalid expression syntax: {err.msg}") from err

    evaluator = SafeExpressionEvaluator()
    return evaluator.visit(parsed)
