from pathlib import Path

import mysql.connector

from connection import mysql_settings


SCHEMA_FILE = Path(__file__).parent / "database" / "schema.sql"


def initialize_database() -> None:
    settings = mysql_settings()
    database = str(settings["database"])
    server_settings = {
        key: value for key, value in settings.items() if key != "database"
    }

    server_connection = mysql.connector.connect(**server_settings)
    server_cursor = server_connection.cursor()
    try:
        quoted_database = f"`{database.replace('`', '``')}`"
        server_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {quoted_database}")
        server_connection.commit()
    except Exception:
        server_connection.rollback()
        raise
    finally:
        server_cursor.close()
        server_connection.close()

    database_connection = mysql.connector.connect(**settings)
    database_cursor = database_connection.cursor()
    try:
        schema = SCHEMA_FILE.read_text(encoding="utf-8")
        for statement in schema.split(";"):
            statement = statement.strip()
            if statement:
                database_cursor.execute(statement)
        database_connection.commit()
    except Exception:
        database_connection.rollback()
        raise
    finally:
        database_cursor.close()
        database_connection.close()


if __name__ == "__main__":
    initialize_database()
    print("Attendance database initialized successfully.")
