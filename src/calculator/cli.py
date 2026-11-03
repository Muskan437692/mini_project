"""Interactive and non-interactive Command Line Interface for the Calculator."""

import argparse
import sys
from typing import List, Optional

from calculator.engine import Calculator, evaluate
from calculator.exceptions import CalculatorError


def format_number(val: float) -> str:
    """Format number cleanly (e.g. 5.0 -> '5', 5.25 -> '5.25')."""
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    return f"{val:g}"


HELP_TEXT = """
Available commands in REPL mode:
  <expression>          Evaluate an expression (e.g., '3 + 4 * 2', 'sqrt(25)', '2 ^ 8')
  add <val>             Add <val> to running value
  sub <val>             Subtract <val> from running value
  mul <val>             Multiply running value by <val>
  div <val>             Divide running value by <val>
  mod <val>             Modulo running value by <val>
  pow <val>             Raise running value to power of <val>
  sqrt                  Take square root of running value
  ms / store            Store running value to memory
  mr / recall           Recall value from memory
  m+                    Add running value to memory
  m-                    Subtract running value from memory
  mc                    Clear memory
  history               Show calculation history
  clear / reset         Reset running value to 0
  help                  Show this help message
  quit / exit / q       Exit the calculator
"""


def repl(calculator: Optional[Calculator] = None) -> None:
    """Run interactive Read-Eval-Print Loop."""
    calc = calculator or Calculator()
    print("Simple Calculator CLI (Type 'help' for commands, 'quit' to exit)")
    print(f"Current Value: {format_number(calc.current_value)}")

    while True:
        try:
            raw_line = input("calc> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not raw_line:
            continue

        parts = raw_line.split()
        cmd = parts[0].lower()

        if cmd in ("exit", "quit", "q"):
            print("Goodbye!")
            break
        elif cmd in ("help", "?"):
            print(HELP_TEXT)
            continue
        elif cmd == "history":
            if not calc.history:
                print("No calculations in history.")
            else:
                for idx, item in enumerate(calc.history, 1):
                    print(f" {idx}. {item.expression_or_op} = {format_number(item.result)}")
            continue
        elif cmd in ("clear", "reset"):
            val = calc.reset()
            print(f"= {format_number(val)}")
            continue
        elif cmd in ("ms", "store"):
            val = calc.memory_store()
            print(f"Memory Stored: {format_number(val)}")
            continue
        elif cmd in ("mr", "recall"):
            val = calc.memory_recall()
            print(f"= {format_number(val)}")
            continue
        elif cmd == "m+":
            val = calc.memory_add()
            print(f"Memory: {format_number(val)}")
            continue
        elif cmd == "m-":
            val = calc.memory_subtract()
            print(f"Memory: {format_number(val)}")
            continue
        elif cmd == "mc":
            calc.memory_clear()
            print("Memory Cleared.")
            continue
        elif cmd == "sqrt":
            try:
                res = calc.square_root()
                print(f"= {format_number(res)}")
            except CalculatorError as e:
                print(f"Error: {e}")
            continue

        # Single operations with argument like 'add 5', 'mul 2'
        op_map = {
            "add": calc.add,
            "sub": calc.subtract,
            "mul": calc.multiply,
            "div": calc.divide,
            "mod": calc.modulo,
            "pow": calc.power,
        }
        if cmd in op_map:
            if len(parts) != 2:
                print(f"Error: '{cmd}' requires exactly one numeric argument.")
                continue
            try:
                arg_val = float(parts[1]) if "." in parts[1] else int(parts[1])
                res = op_map[cmd](arg_val)
                print(f"= {format_number(res)}")
            except ValueError:
                print(f"Error: Invalid number '{parts[1]}'.")
            except CalculatorError as e:
                print(f"Error: {e}")
            continue

        # Otherwise evaluate as an expression
        try:
            res = calc.evaluate_expression(raw_line)
            print(f"= {format_number(res)}")
        except CalculatorError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: Unexpected error ({e})")


def main(argv: Optional[List[str]] = None) -> int:
    """Entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="calculator",
        description="A simple, robust command-line calculator.",
    )
    parser.add_argument(
        "-e",
        "--eval",
        dest="expression",
        metavar="EXPR",
        type=str,
        help="Evaluate a mathematical expression directly and exit.",
    )
    parser.add_argument(
        "expression_args",
        nargs="*",
        help="Optional expression arguments to evaluate directly (if provided).",
    )

    args = parser.parse_args(argv)

    if args.expression:
        expr = args.expression
    elif args.expression_args:
        expr = " ".join(args.expression_args)
    else:
        expr = None

    if expr is not None:
        try:
            result = evaluate(expr)
            print(format_number(result))
            return 0
        except CalculatorError as err:
            print(f"Error: {err}", file=sys.stderr)
            return 1
        except Exception as err:
            print(f"Error: {err}", file=sys.stderr)
            return 1

    repl()
    return 0


if __name__ == "__main__":
    sys.exit(main())
