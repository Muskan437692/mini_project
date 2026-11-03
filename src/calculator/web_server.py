"""Simple and lightweight HTTP web server for the Calculator frontend and backend API."""

import json
import mimetypes
import os
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from typing import Optional
from urllib.parse import urlparse

from calculator.engine import Calculator, evaluate
from calculator.exceptions import CalculatorError

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
_GLOBAL_CALCULATOR = Calculator()


class CalculatorHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Handles calculator REST API calls and serves static web assets."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/history":
            history_data = [
                {"expression": item.expression_or_op, "result": item.result}
                for item in _GLOBAL_CALCULATOR.history
            ]
            self._send_json({"history": history_data})
            return
        elif parsed.path == "/api/state":
            self._send_json({
                "current_value": _GLOBAL_CALCULATOR.current_value,
                "memory": _GLOBAL_CALCULATOR.memory,
            })
            return

        super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)

        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            payload = json.loads(raw_body.decode("utf-8")) if raw_body else {}
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON body"}, status=HTTPStatus.BAD_REQUEST)
            return

        if parsed.path == "/api/evaluate":
            expr = payload.get("expression")
            if not expr or not isinstance(expr, str):
                self._send_json({"error": "Missing or invalid 'expression' field"}, status=HTTPStatus.BAD_REQUEST)
                return
            try:
                result = _GLOBAL_CALCULATOR.evaluate_expression(expr)
                self._send_json({"result": result, "expression": expr})
            except CalculatorError as err:
                self._send_json({"error": str(err)}, status=HTTPStatus.BAD_REQUEST)
            except Exception as err:
                self._send_json({"error": f"Internal server error: {err}"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
            return

        elif parsed.path == "/api/reset":
            val = _GLOBAL_CALCULATOR.reset()
            self._send_json({"current_value": val})
            return

        elif parsed.path == "/api/clear_history":
            _GLOBAL_CALCULATOR.clear_history()
            self._send_json({"message": "History cleared"})
            return

        elif parsed.path == "/api/memory":
            action = payload.get("action")
            try:
                if action == "store":
                    val = _GLOBAL_CALCULATOR.memory_store()
                elif action == "recall":
                    val = _GLOBAL_CALCULATOR.memory_recall()
                elif action == "add":
                    val = _GLOBAL_CALCULATOR.memory_add()
                elif action == "subtract":
                    val = _GLOBAL_CALCULATOR.memory_subtract()
                elif action == "clear":
                    _GLOBAL_CALCULATOR.memory_clear()
                    val = 0
                else:
                    self._send_json({"error": f"Unknown memory action: {action}"}, status=HTTPStatus.BAD_REQUEST)
                    return
                self._send_json({
                    "memory": _GLOBAL_CALCULATOR.memory,
                    "current_value": _GLOBAL_CALCULATOR.current_value,
                })
            except CalculatorError as err:
                self._send_json({"error": str(err)}, status=HTTPStatus.BAD_REQUEST)
            return

        self._send_json({"error": "Endpoint not found"}, status=HTTPStatus.NOT_FOUND)

    def _send_json(self, data: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def create_server(host: str = "0.0.0.0", port: int = 8000) -> ThreadingHTTPServer:
    """Create and return a configured HTTP server."""
    return ThreadingHTTPServer((host, port), CalculatorHTTPRequestHandler)


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    """Run the web server."""
    server = create_server(host, port)
    print(f"Calculator Web Application running on http://{host}:{port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.shutdown()


if __name__ == "__main__":
    run_server()
