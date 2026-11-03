"""Tests for the Calculator web backend server API."""

import json
import threading
import time
import unittest
from http.client import HTTPConnection

from calculator.web_server import create_server


class TestWebServerAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Bind to port 0 so the OS assigns an available ephemeral port
        cls.server = create_server("127.0.0.1", 0)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.1)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def _request(self, method: str, path: str, body: dict = None):
        conn = HTTPConnection("127.0.0.1", self.port)
        headers = {"Content-Type": "application/json"} if body else {}
        data = json.dumps(body) if body else None
        conn.request(method, path, body=data, headers=headers)
        res = conn.getresponse()
        raw = res.read().decode("utf-8")
        conn.close()
        return res.status, raw

    def test_static_index_html(self):
        status, body = self._request("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn("Calculator Web Application", body)

    def test_api_evaluate_success(self):
        status, body = self._request("POST", "/api/evaluate", {"expression": "25 * 4 + 10"})
        self.assertEqual(status, 200)
        data = json.loads(body)
        self.assertEqual(data["result"], 110)

    def test_api_evaluate_error(self):
        status, body = self._request("POST", "/api/evaluate", {"expression": "10 / 0"})
        self.assertEqual(status, 400)
        data = json.loads(body)
        self.assertIn("Cannot divide by zero", data["error"])

    def test_api_memory_lifecycle(self):
        # Store
        self._request("POST", "/api/evaluate", {"expression": "50"})
        status, body = self._request("POST", "/api/memory", {"action": "store"})
        self.assertEqual(status, 200)
        data = json.loads(body)
        self.assertEqual(data["memory"], 50)

        # Clear
        status, body = self._request("POST", "/api/memory", {"action": "clear"})
        self.assertEqual(status, 200)
        data = json.loads(body)
        self.assertEqual(data["memory"], 0)

    def test_api_history(self):
        self._request("POST", "/api/evaluate", {"expression": "7 * 6"})
        status, body = self._request("GET", "/api/history")
        self.assertEqual(status, 200)
        data = json.loads(body)
        self.assertTrue(len(data["history"]) > 0)


if __name__ == "__main__":
    unittest.main()
