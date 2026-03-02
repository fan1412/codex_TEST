"""MariaDB access helpers and schema-driven select function generator."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

import pymysql
from pymysql.cursors import DictCursor


@dataclass(frozen=True)
class DBConfig:
    host: str = "172.18.1.65"
    port: int = 3306
    user: str = "zxfc_admin"
    password: str = "WGZXwgzx669992"
    database: str = ""
    charset: str = "utf8mb4"


class MariaDBClient:
    """Thin client wrapper for MariaDB queries."""

    def __init__(self, config: DBConfig):
        self._config = config

    def connect(self):
        return pymysql.connect(
            host=self._config.host,
            port=self._config.port,
            user=self._config.user,
            password=self._config.password,
            database=self._config.database or None,
            charset=self._config.charset,
            cursorclass=DictCursor,
        )

    def fetch_columns(self, table_name: str, schema_name: str) -> list[str]:
        sql = """
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
        ORDER BY ORDINAL_POSITION
        """
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (schema_name, table_name))
                return [row["COLUMN_NAME"] for row in cur.fetchall()]

    def select_all(self, table_name: str, limit: int | None = None) -> list[dict[str, Any]]:
        query = f"SELECT * FROM `{table_name}`"
        params: list[Any] = []
        if limit is not None:
            query += " LIMIT %s"
            params.append(limit)

        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return list(cur.fetchall())

    def select_by_filters(self, table_name: str, filters: dict[str, Any]) -> list[dict[str, Any]]:
        if not filters:
            return self.select_all(table_name)

        where_clause = " AND ".join(f"`{key}` = %s" for key in filters)
        query = f"SELECT * FROM `{table_name}` WHERE {where_clause}"
        params = list(filters.values())

        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return list(cur.fetchall())


class SelectFunctionGenerator:
    """Generate python select helper functions from table structures."""

    def __init__(self, client: MariaDBClient):
        self.client = client

    def _build_function_source(self, table_name: str, columns: Iterable[str]) -> str:
        args = ", ".join(f"{col}=None" for col in columns)
        filters = "\n".join(
            f"    if {col} is not None:\n        filters['{col}'] = {col}" for col in columns
        )
        return f'''
def select_{table_name}(client, {args}):
    """Schema-based select function for {table_name}."""
    filters = {{}}
{filters if filters else '    pass'}
    return client.select_by_filters("{table_name}", filters)
'''.strip("\n")

    def generate(self, schema_name: str, table_names: list[str]) -> str:
        blocks = [
            '"""Auto-generated select functions from MariaDB table schemas."""',
            "",
        ]
        for table in table_names:
            columns = self.client.fetch_columns(table, schema_name)
            blocks.append(self._build_function_source(table, columns))
            blocks.append("")
        return "\n".join(blocks).rstrip() + "\n"
