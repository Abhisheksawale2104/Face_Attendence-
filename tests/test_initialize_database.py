import os
import unittest
from unittest.mock import MagicMock, call, patch

from initialize_database import initialize_database


class InitializeDatabaseTests(unittest.TestCase):
    def test_creates_database_and_applies_schema(self) -> None:
        server_connection = MagicMock()
        database_connection = MagicMock()
        server_cursor = server_connection.cursor.return_value
        database_cursor = database_connection.cursor.return_value
        environment = {
            "MYSQL_HOST": "127.0.0.1",
            "MYSQL_PORT": "3306",
            "MYSQL_USER": "attendance_app",
            "MYSQL_PASSWORD": "local-test-password",
            "MYSQL_DATABASE": "school`attendance",
        }

        with (
            patch.dict(os.environ, environment, clear=True),
            patch(
                "initialize_database.mysql.connector.connect",
                side_effect=[server_connection, database_connection],
            ) as connect,
        ):
            initialize_database()

        self.assertEqual(
            server_cursor.execute.call_args,
            call("CREATE DATABASE IF NOT EXISTS `school``attendance`"),
        )
        self.assertEqual(
            connect.call_args_list,
            [
                call(
                    host="127.0.0.1",
                    port=3306,
                    user="attendance_app",
                    password="local-test-password",
                ),
                call(
                    host="127.0.0.1",
                    port=3306,
                    user="attendance_app",
                    password="local-test-password",
                    database="school`attendance",
                ),
            ],
        )
        self.assertEqual(database_cursor.execute.call_count, 2)
        server_connection.commit.assert_called_once()
        database_connection.commit.assert_called_once()
        server_connection.close.assert_called_once()
        database_connection.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
