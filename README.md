# Simple Calculator

A modular, well-structured, and safe Python calculator with both an interactive Command-Line Interface (CLI) and an easy-to-use Python library API.

---

## Features

- **Standard Arithmetic Operations**: Addition, subtraction, multiplication, division, modulo, exponentiation (using `^` or `**`), and square root (`sqrt`).
- **Safe Expression Evaluation**: Expression evaluation powered by Python's Abstract Syntax Tree (`ast`), completely avoiding unsafe `eval()`.
- **Stateful Calculator Engine**:
  - Running result accumulation.
  - Full memory functions: Memory Store (`ms`), Memory Recall (`mr`), Memory Addition (`m+`), Memory Subtraction (`m-`), Memory Clear (`mc`).
  - History tracking and inspection.
- **Interactive REPL & Direct CLI**:
  - Evaluate expressions non-interactively via `-e / --eval` or command-line arguments.
  - Interactive REPL with built-in help and history display.
- **Robust Error Handling**: Dedicated custom exception hierarchy for division by zero, negative square roots, and malformed inputs.
- **Comprehensive Test Suite**: 100% standard library `unittest` suite.

---

## Project Structure

```
.
├── pyproject.toml              # Build & packaging configuration
├── README.md                   # Project overview & documentation
├── src/
│   └── calculator/
│       ├── __init__.py         # Public exports (Calculator, evaluate, operations, exceptions)
│       ├── __main__.py         # Module execution entrypoint (python -m calculator)
│       ├── cli.py              # CLI parser, REPL interface, output formatter
│       ├── engine.py           # Calculator class, history, SafeExpressionEvaluator
│       ├── exceptions.py       # Custom exception hierarchy
│       └── operations.py       # Validated arithmetic operations
└── tests/
    ├── __init__.py
    ├── test_cli.py             # CLI flags and REPL integration tests
    ├── test_engine.py          # Calculator state, memory, and AST expression tests
    └── test_operations.py      # Core arithmetic & boundary test cases
```

---

## Installation & Setup

No third-party runtime dependencies are required—the project relies solely on the Python 3 standard library.

Install in editable mode:
```bash
pip install -e .
```

---

## Usage

### 1. Command-Line Interface (CLI)

#### Direct Evaluation:
```bash
# Using flag -e
calculator -e "2 + 3 * 4"
# Output: 14

# Or via python -m calculator
python3 -m calculator -e "sqrt(144) + 2 ^ 3"
# Output: 20

# Directly passing expression arguments
python3 -m calculator "10 / (2 + 3)"
# Output: 2
```

#### Interactive REPL:
Launch interactive mode by running `calculator` or `python3 -m calculator`:

```
Simple Calculator CLI (Type 'help' for commands, 'quit' to exit)
Current Value: 0
calc> 25 * 4
= 100
calc> add 50
= 150
calc> ms
Memory Stored: 150
calc> clear
= 0
calc> mr
= 150
calc> sqrt
= 12.2474
calc> history
 1. 25 * 4 = 100
 2. 100 + 50 = 150
 3. sqrt(150) = 12.2474
calc> quit
Goodbye!
```

---

### 2. Python API

#### Evaluating String Expressions
```python
from calculator import evaluate

result = evaluate("(5 + 3) * 2 ^ 3")
print(result)  # 64
```

#### Using the Stateful Calculator
```python
from calculator import Calculator

calc = Calculator(10)
calc.add(5)          # 15
calc.multiply(2)     # 30
calc.square_root()   # 5.477225575051661

# Memory
calc.memory_store()  # stores current value in memory
calc.reset(0)        # resets running total
calc.memory_recall() # recalls 5.477225575051661

# History
for entry in calc.history:
    print(f"{entry.expression_or_op} = {entry.result}")
```

#### Individual Operations
```python
from calculator import add, divide, square_root
from calculator.exceptions import DivisionByZeroError

print(add(10, 20))  # 30
print(divide(20, 4))  # 5.0

try:
    divide(1, 0)
except DivisionByZeroError as err:
    print("Handled safely:", err)
```

---

## Running Tests

Run the full automated test suite using `unittest`:

```bash
PYTHONPATH=src python3 -m unittest discover tests
```
