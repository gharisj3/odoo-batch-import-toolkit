"""Safe PostgreSQL batch insert helpers."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from itertools import islice
from typing import Iterable, Iterator, Sequence

from .reporting import ImportSummary
from .validators import quote_identifier, validate_batch_size, validate_identifier

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class BatchInsertPlan:
    table: str
    columns: list[str]
    rows_seen: int
    batch_size: int
    dry_run: bool


def chunks(iterable: Iterable[dict[str, object]], size: int) -> Iterator[list[dict[str, object]]]:
    iterator = iter(iterable)
    while True:
        chunk = list(islice(iterator, size))
        if not chunk:
            break
        yield chunk


def infer_columns(rows: Sequence[dict[str, object]]) -> list[str]:
    if not rows:
        return []
    columns = list(rows[0].keys())
    for column in columns:
        validate_identifier(column, label="column")
    return columns


def build_insert_sql(table: str, columns: Sequence[str]) -> str:
    if not columns:
        raise ValueError("Cannot build INSERT statement without columns.")
    quoted_table = quote_identifier(table)
    quoted_columns = ", ".join(quote_identifier(column) for column in columns)
    placeholders = ", ".join(["%s"] * len(columns))
    return f"INSERT INTO {quoted_table} ({quoted_columns}) VALUES ({placeholders})"


def rows_to_payload(rows: Sequence[dict[str, object]], columns: Sequence[str]) -> list[tuple[object, ...]]:
    return [tuple(row.get(column) for column in columns) for row in rows]


def ensure_direct_write_allowed(table: str, *, allow_direct_table_write: bool) -> None:
    is_staging = table.startswith("staging_") or ".staging_" in table
    if not is_staging and not allow_direct_table_write:
        raise PermissionError(
            "Direct writes to non-staging tables are disabled. Use a staging_* table "
            "or pass --allow-direct-table-write after reviewing Odoo ORM bypass risks."
        )


def batch_insert(
    conn: object | None,
    table: str,
    rows: Iterable[dict[str, object]],
    *,
    batch_size: int = 1000,
    dry_run: bool = True,
    allow_direct_table_write: bool = False,
) -> ImportSummary:
    validate_batch_size(batch_size)
    quote_identifier(table)
    ensure_direct_write_allowed(table, allow_direct_table_write=allow_direct_table_write)

    rows_seen = 0
    rows_inserted = 0
    start = time.perf_counter()

    try:
        for chunk in chunks(rows, batch_size):
            rows_seen += len(chunk)
            columns = infer_columns(chunk)
            sql = build_insert_sql(table, columns)
            payload = rows_to_payload(chunk, columns)

            if dry_run:
                LOGGER.info("Dry run: would execute %s with %s rows", sql, len(payload))
                continue
            if conn is None:
                raise ValueError("A database connection is required when dry_run is false.")
            with conn.cursor() as cursor:
                cursor.executemany(sql, payload)
            rows_inserted += len(payload)

        if not dry_run and conn is not None:
            conn.commit()
    except Exception:
        if not dry_run and conn is not None:
            conn.rollback()
        raise

    if dry_run:
        rows_inserted = rows_seen
    elapsed = time.perf_counter() - start
    return ImportSummary(
        table=table,
        rows_seen=rows_seen,
        rows_inserted=rows_inserted,
        batch_size=batch_size,
        dry_run=dry_run,
        elapsed_seconds=elapsed,
    )
