import os
from collections.abc import Sequence

import mysql.connector


def mysql_settings() -> dict[str, str | int]:
    user = os.environ.get("MYSQL_USER", "").strip()
    if not user:
        raise ValueError("Set MYSQL_USER before connecting to the attendance database.")

    try:
        port = int(os.environ.get("MYSQL_PORT", "3306"))
    except ValueError as exc:
        raise ValueError("MYSQL_PORT must be a number between 1 and 65535.") from exc
    if not 1 <= port <= 65535:
        raise ValueError("MYSQL_PORT must be a number between 1 and 65535.")

    return {
        "host": os.environ.get("MYSQL_HOST", "127.0.0.1"),
        "port": port,
        "user": user,
        "password": os.environ.get("MYSQL_PASSWORD", ""),
        "database": os.environ.get("MYSQL_DATABASE", "attendance"),
    }


class MysqlConnection:
    def __init__(self) -> None:
        self.conn = mysql.connector.connect(**mysql_settings())

    def __enter__(self) -> "MysqlConnection":
        return self

    def __exit__(self, *exc_info: object) -> None:
        if any(value is not None for value in exc_info):
            self.conn.rollback()
        self.close()

    def insert(self, sql_query: str, values: Sequence[object]) -> None:
        self._execute(sql_query, values)

    def read(
        self, sql_query: str, values: Sequence[object] | None = None
    ) -> list[tuple[object, ...]]:
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql_query, values)
            return cursor.fetchall()
        finally:
            cursor.close()

    def create(self, sql_query: str) -> None:
        self._execute(sql_query)

    def update(self, sql_query: str, values: Sequence[object]) -> None:
        self._execute(sql_query, values)

    def delete(self, sql_query: str, values: Sequence[object]) -> None:
        self._execute(sql_query, values)

    def _execute(
        self, sql_query: str, values: Sequence[object] | None = None
    ) -> None:
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql_query, values)
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
        finally:
            cursor.close()

    def close(self) -> None:
        self.conn.close()
