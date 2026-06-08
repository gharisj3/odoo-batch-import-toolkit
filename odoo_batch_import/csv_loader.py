"""Streaming CSV loading utilities."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterator, Sequence

from .validators import ValidationResult, validate_headers


def normalize_value(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value if value != "" else None


def stream_csv_rows(path: str | Path, *, required_headers: Sequence[str] | None = None) -> Iterator[dict[str, object]]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        result = validate_headers(headers, required_headers)
        if not result.ok:
            raise ValueError("; ".join(result.errors))
        for row in reader:
            yield {key: normalize_value(value) for key, value in row.items()}


def read_headers(path: str | Path) -> list[str]:
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        return next(reader, [])


def validate_csv_file(path: str | Path, *, required_headers: Sequence[str] | None = None) -> ValidationResult:
    try:
        headers = read_headers(path)
        return validate_headers(headers, required_headers)
    except OSError as exc:
        return ValidationResult(ok=False, errors=[str(exc)])
