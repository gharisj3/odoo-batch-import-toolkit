import pytest

from odoo_batch_import.batch_insert import batch_insert, build_insert_sql, rows_to_payload


def test_build_insert_sql_quotes_identifiers():
    sql = build_insert_sql("staging_partner_import", ["name", "email"])

    assert sql == 'INSERT INTO "staging_partner_import" ("name", "email") VALUES (%s, %s)'


def test_rows_to_payload_preserves_column_order():
    payload = rows_to_payload([{"email": "a@example.com", "name": "Alice"}], ["name", "email"])

    assert payload == [("Alice", "a@example.com")]


def test_dry_run_counts_rows_without_connection():
    summary = batch_insert(None, "staging_partner_import", [{"name": "Alice"}], dry_run=True)

    assert summary.rows_seen == 1
    assert summary.rows_inserted == 1
    assert summary.dry_run is True


def test_direct_write_requires_explicit_flag():
    with pytest.raises(PermissionError):
        batch_insert(None, "res_partner", [{"name": "Alice"}], dry_run=True)
