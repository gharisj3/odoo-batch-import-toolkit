"""Validation helpers shared by CLI, loader, and batch insert modules."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Sequence


IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ALLOWED_MODES = {"staging", "direct"}


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    errors: list[str]


def validate_identifier(identifier: str, *, label: str = "identifier") -> None:
    if not identifier or not IDENTIFIER_RE.match(identifier):
        raise ValueError(f"Invalid {label}: {identifier!r}")


def validate_qualified_identifier(identifier: str, *, label: str = "identifier") -> None:
    parts = identifier.split(".")
    if len(parts) > 2:
        raise ValueError(f"Invalid {label}: {identifier!r}")
    for part in parts:
        validate_identifier(part, label=label)


def quote_identifier(identifier: str) -> str:
    validate_qualified_identifier(identifier)
    return ".".join(f'"{part}"' for part in identifier.split("."))


def validate_headers(headers: Sequence[str], required: Iterable[str] | None = None) -> ValidationResult:
    errors: list[str] = []
    seen: set[str] = set()
    for header in headers:
        if not header:
            errors.append("CSV contains an empty header.")
        elif header in seen:
            errors.append(f"CSV contains duplicate header: {header}")
        else:
            seen.add(header)
    for required_header in required or []:
        if required_header not in seen:
            errors.append(f"Missing required header: {required_header}")
    return ValidationResult(ok=not errors, errors=errors)


def validate_required_fields(row: dict[str, object], required: Iterable[str]) -> list[str]:
    errors: list[str] = []
    for field in required:
        value = row.get(field)
        if value is None or value == "":
            errors.append(f"Missing required field: {field}")
    return errors


def validate_email(value: str | None) -> bool:
    if not value:
        return True
    return bool(EMAIL_RE.match(value))


def validate_batch_size(batch_size: int) -> None:
    if batch_size < 1 or batch_size > 100_000:
        raise ValueError("Batch size must be between 1 and 100000.")


def validate_mode(mode: str) -> None:
    if mode not in ALLOWED_MODES:
        raise ValueError(f"Invalid mode {mode!r}. Expected one of: {', '.join(sorted(ALLOWED_MODES))}.")


def validate_rows(rows: Iterable[dict[str, object]], required: Iterable[str] | None = None) -> ValidationResult:
    errors: list[str] = []
    for index, row in enumerate(rows, start=2):
        for message in validate_required_fields(row, required or []):
            errors.append(f"Row {index}: {message}")
        email = row.get("email")
        if isinstance(email, str) and not validate_email(email):
            errors.append(f"Row {index}: Invalid email: {email}")
    return ValidationResult(ok=not errors, errors=errors)
