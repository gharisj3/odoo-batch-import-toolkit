import pytest

from odoo_batch_import.validators import validate_batch_size, validate_email, validate_identifier, validate_rows


def test_validate_identifier_rejects_unsafe_value():
    with pytest.raises(ValueError):
        validate_identifier("res_partner;drop table")


def test_validate_email_lightweight():
    assert validate_email("a@example.com")
    assert not validate_email("not-an-email")


def test_validate_required_fields():
    result = validate_rows([{"name": "", "email": "bad"}], required=["name"])

    assert not result.ok
    assert "Row 2: Missing required field: name" in result.errors
    assert "Row 2: Invalid email: bad" in result.errors


def test_validate_batch_size_bounds():
    with pytest.raises(ValueError):
        validate_batch_size(0)
