"""EXPLAIN ANALYZE helpers."""

from __future__ import annotations

from pathlib import Path


def read_sql_file(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def split_sql_statements(sql: str) -> list[str]:
    return [statement.strip() for statement in sql.split(";") if statement.strip()]


def explain_analyze(conn: object, sql: str) -> list[str]:
    statements = split_sql_statements(sql)
    plans: list[str] = []
    with conn.cursor() as cursor:
        for statement in statements:
            cursor.execute("EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) " + statement)
            plans.append("\n".join(row[0] for row in cursor.fetchall()))
    return plans
