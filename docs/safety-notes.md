# Safety Notes

Raw SQL risks in Odoo:

- Bypasses ORM create/write overrides.
- May skip computed field updates and inverse methods.
- Can miss automated actions, mail tracking, and module-specific side effects.
- Can break relational consistency if required columns or links are missing.
- Can create records that look present in PostgreSQL but behave incorrectly in Odoo.

Direct writes may be acceptable only for well-understood technical tables, disposable benchmark tables, or carefully reviewed maintenance operations.

Staging tables are safer because they preserve the original payload, allow validation and duplicate detection, and let Odoo process final records through ORM logic.

Before real imports:

- Back up the database.
- Test in a staging environment.
- Use transactions and verify rollback behavior.
- Keep an audit trail with `external_ref`, `status`, `error_message`, and timestamps.
- Design idempotency around external references.
