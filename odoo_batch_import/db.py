"""PostgreSQL connection helpers."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from .config import PostgresConfig


@contextmanager
def connect(config: PostgresConfig) -> Iterator[object]:
    import psycopg2

    conn = psycopg2.connect(config.dsn())
    try:
        yield conn
    finally:
        conn.close()
