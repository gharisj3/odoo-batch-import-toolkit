# Architecture

```text
CSV File
  -> CLI Validator
  -> Batch Insert Engine
  -> PostgreSQL Staging Table
  -> Odoo Abstract Mixin
  -> ORM-safe Record Creation
  -> Benchmark Report
```

The CLI validates headers and common row-level fields before preparing batches. The batch insert engine validates table and column identifiers, builds parameterized SQL, and supports dry-run mode. PostgreSQL staging tables hold raw imported data plus status fields. Odoo modules can inherit the abstract mixin to process pending staged rows through normal ORM `create` or `write` logic.

This keeps high-volume loading separate from business-rule execution.
