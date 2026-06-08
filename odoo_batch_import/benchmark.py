"""Benchmark helpers that do not require Odoo."""

from __future__ import annotations

import time
from pathlib import Path

from .batch_insert import batch_insert
from .csv_loader import stream_csv_rows
from .reporting import benchmark_markdown


def run_dry_run_benchmark(csv_file: str | Path, table: str, *, batch_size: int) -> str:
    start = time.perf_counter()
    summary = batch_insert(None, table, stream_csv_rows(csv_file), batch_size=batch_size, dry_run=True)
    runtime = time.perf_counter() - start
    rows = [
        {
            "scenario": "dry-run payload preparation",
            "records": summary.rows_seen,
            "batch_size": batch_size,
            "runtime": runtime,
            "rows_per_second": summary.rows_seen / runtime if runtime else 0,
            "notes": "No database connection used.",
        }
    ]
    return benchmark_markdown("Odoo Batch Import Benchmark", rows)
