from pathlib import Path

from odoo_batch_import.csv_loader import stream_csv_rows, validate_csv_file


def test_stream_csv_rows_normalizes_empty_strings(tmp_path: Path):
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("name,email\nAlice,\n", encoding="utf-8")

    rows = list(stream_csv_rows(csv_file, required_headers=["name"]))

    assert rows == [{"name": "Alice", "email": None}]


def test_validate_csv_file_reports_missing_header(tmp_path: Path):
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("name\nAlice\n", encoding="utf-8")

    result = validate_csv_file(csv_file, required_headers=["email"])

    assert not result.ok
    assert "Missing required header: email" in result.errors
