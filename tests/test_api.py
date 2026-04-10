import os
import tempfile
import unittest


class ApiTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 测试前设置独立数据库，避免污染教学数据
        cls.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        cls.temp_db.close()
        os.environ["DATABASE_PATH"] = cls.temp_db.name

        from backend.app import create_app

        cls.app = create_app()
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        # 测试结束后清理临时数据库文件
        if os.path.exists(cls.temp_db.name):
            os.remove(cls.temp_db.name)

    def test_login(self):
        response = self.client.post(
            "/api/login", json={"username": "admin", "password": "admin123"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.get_json()["success"])

    def test_latest_sensor(self):
        response = self.client.get("/api/sensors/latest")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("temperature", payload["data"])

    def test_analysis(self):
        response = self.client.get("/api/analysis")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("score", payload["data"])


if __name__ == "__main__":
    unittest.main()
