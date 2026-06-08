"""Small terminal and markdown reporting helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ImportSummary:
    table: str
    rows_seen: int
    rows_inserted: int
    batch_size: int
    dry_run: bool
    elapsed_seconds: float

    @property
    def rows_per_second(self) -> float:
        if self.elapsed_seconds <= 0:
            return 0.0
        return self.rows_inserted / self.elapsed_seconds


def print_summary(summary: ImportSummary) -> None:
    print(f"Table: {summary.table}")
    print(f"Rows seen: {summary.rows_seen}")
    print(f"Rows inserted: {summary.rows_inserted}")
    print(f"Batch size: {summary.batch_size}")
    print(f"Dry run: {summary.dry_run}")
    print(f"Elapsed: {summary.elapsed_seconds:.4f}s")
    print(f"Rows/sec: {summary.rows_per_second:.2f}")


def benchmark_markdown(title: str, rows: list[dict[str, object]]) -> str:
    lines = [f"# {title}", "", "| Scenario | Records | Batch size | Runtime | Rows/sec | Notes |", "| --- | ---: | ---: | ---: | ---: | --- |"]
    for row in rows:
        lines.append(
            f"| {row['scenario']} | {row['records']} | {row['batch_size']} | "
            f"{float(row['runtime']):.4f}s | {float(row['rows_per_second']):.2f} | {row.get('notes', '')} |"
        )
    return "\n".join(lines) + "\n"
