# Simple Calculator & Web Application

A modular, well-structured, and safe Python calculator featuring an interactive Web Application (Frontend & Backend API), a Command-Line Interface (CLI), and a clean Python library API.

---

## Features

- **Web Application (Frontend + Backend)**:
  - Modern, responsive UI with calculator layout, display, keypad, memory controls, and history list.
  - Interactive evaluation, click-to-recall history entries, and keyboard navigation.
  - Built-in lightweight HTTP web server and REST API (`/api/evaluate`, `/api/memory`, `/api/history`, `/api/reset`).
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
- **Comprehensive Test Suite**: 100% standard library `unittest` suite testing operations, engine, CLI, and web server API.

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
│       ├── operations.py       # Validated arithmetic operations
│       ├── web_server.py       # Lightweight HTTP REST API server & static file server
│       └── static/             # Web Frontend assets
│           ├── index.html      # Calculator single-page web app
│           ├── style.css       # Responsive dark-theme styling
│           └── app.js          # Interactive frontend client
└── tests/
    ├── __init__.py
    ├── test_cli.py             # CLI flags and REPL integration tests
    ├── test_engine.py          # Calculator state, memory, and AST expression tests
    ├── test_operations.py      # Core arithmetic & boundary test cases
    └── test_web.py             # HTTP server and REST API tests
```

---

## Running the Web Application

Start the web server:
```bash
PYTHONPATH=src python3 src/calculator/web_server.py
```
Then open your browser to `http://localhost:8000/`.

---

## Command-Line Interface (CLI)

#### Direct Evaluation:
```bash
python3 -m calculator -e "sqrt(144) + 2 ^ 3"
# Output: 20
```

#### Interactive REPL:
```bash
python3 -m calculator
```

---

## Running Tests

Run the full automated test suite using `unittest`:

```bash
PYTHONPATH=src python3 -m unittest discover tests
```
