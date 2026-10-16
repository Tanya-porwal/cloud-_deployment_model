import os
import unittest
from unittest.mock import patch

from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_home_displays_configured_name_and_version(self):
        with patch.dict(os.environ, {"APP_NAME": "Ada Lovelace", "APP_VERSION": "2.4.1"}):
            response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to the Cloud Deployment Lab", response.data)
        self.assertIn(b"Ada Lovelace", response.data)
        self.assertIn(b"2.4.1", response.data)

    def test_home_uses_defaults(self):
        with patch.dict(os.environ, {}, clear=True):
            response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Tanya Porwal", response.data)
        self.assertIn(b"1.0.0", response.data)

    def test_health_check(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
