import unittest
from flask_testing import TestCase
from app import app

class TestApp(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        return app

    def test_server_is_up_and_running(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
