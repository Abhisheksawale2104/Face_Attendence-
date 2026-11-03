import os
import unittest
from unittest.mock import patch

from connection import mysql_settings


class MysqlSettingsTests(unittest.TestCase):
    def test_reads_connection_settings_from_environment(self) -> None:
        environment = {
            "MYSQL_HOST": "db.example.test",
            "MYSQL_PORT": "3307",
            "MYSQL_USER": "attendance_app",
            "MYSQL_PASSWORD": "local-test-password",
            "MYSQL_DATABASE": "school_attendance",
        }
        with patch.dict(os.environ, environment, clear=True):
            settings = mysql_settings()

        self.assertEqual(
            settings,
            {
                "host": "db.example.test",
                "port": 3307,
                "user": "attendance_app",
                "password": "local-test-password",
                "database": "school_attendance",
            },
        )

    def test_requires_a_database_user(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "MYSQL_USER"):
                mysql_settings()

    def test_rejects_invalid_port(self) -> None:
        for port in ("not-a-number", "0", "65536"):
            with self.subTest(port=port), patch.dict(
                os.environ, {"MYSQL_USER": "attendance_app", "MYSQL_PORT": port}, clear=True
            ):
                with self.assertRaisesRegex(ValueError, "MYSQL_PORT"):
                    mysql_settings()


if __name__ == "__main__":
    unittest.main()
