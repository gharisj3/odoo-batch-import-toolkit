# odoo-batch-import-toolkit

Utilities for validating large CSV imports, loading them into PostgreSQL staging tables, and processing staged rows safely through Odoo ORM helpers.

Normal Odoo imports can become slow around 10,000+ rows because every record may trigger ORM validation, computed fields, access checks, mail/thread behavior, automation, constraints, and module-specific logic. Those protections matter. This toolkit helps technical consultants and Odoo developers separate high-volume data loading from business-safe record creation.

Raw PostgreSQL writes can be powerful, but in Odoo they can bypass ORM business logic, computed fields, constraints, automated actions, mail tracking, access logic, and module-specific behavior. This toolkit therefore recommends raw SQL mainly for staging tables, followed by controlled ORM processing inside Odoo.

## Who this is for

- Odoo technical consultants preparing controlled migrations.
- Backend developers benchmarking import strategies.
- Teams that need repeatable CSV validation and staging-table workflows.
- Developers comparing Odoo ORM imports with raw PostgreSQL loading.

## Architecture

```text
CSV file
  -> CLI validator
  -> batch insert engine
  -> PostgreSQL staging table
  -> Odoo abstract mixin
  -> ORM-safe record creation
  -> benchmark report
```

## Repository structure

```text
odoo_batch_import/                 Python CLI and library modules
odoo_addon/odoo_batch_import_mixin Odoo abstract model mixin addon
scripts/                           Sample generation and benchmark helpers
examples/                          Safe sample CSV/config/report files
sql/                               Staging tables and EXPLAIN examples
tests/                             Unit tests with no live database required
docs/                              Architecture, safety, benchmarking notes
```

## Setup

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and replace placeholder values only in your local copy.

## Environment variables

- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_SSLMODE`
- `ODOO_BASE_URL`
- `ODOO_DATABASE`
- `ODOO_USERNAME`
- `ODOO_PASSWORD`
- `IMPORT_BATCH_SIZE`
- `IMPORT_DRY_RUN`

## CLI usage

Validate a CSV:

```bash
python -m odoo_batch_import.cli validate --file examples/partners_10k_sample.csv --required name email
```

Dry-run a staging insert:

```bash
python -m odoo_batch_import.cli import --file examples/partners_10k_sample.csv --table staging_partner_import --dry-run
```

Direct writes to core Odoo tables are disabled unless explicitly allowed:

```bash
python -m odoo_batch_import.cli import --file examples/partners_10k_sample.csv --table res_partner --allow-direct-table-write --dry-run
```

Run a timing benchmark:

```bash
python -m odoo_batch_import.cli benchmark --file examples/partners_10k_sample.csv --table staging_partner_import --dry-run
```

Run EXPLAIN ANALYZE for a SQL file:

```bash
python -m odoo_batch_import.cli explain --sql sql/explain_analyze_examples.sql
```

When overriding the env file, pass `--env-file` before the subcommand:

```bash
python -m odoo_batch_import.cli --env-file .env validate --file examples/partners_10k_sample.csv
```

## Sample data

The repository includes small safe samples. Generate a larger partner CSV locally:

```bash
python scripts/generate_sample_csv.py --rows 10000 --output examples/generated_partners_10k.csv
```

Generated CSV files are ignored by Git.

## Odoo addon

Copy `odoo_addon/odoo_batch_import_mixin` into an Odoo addons path, update the app list, and install it. Inherit `odoo.batch.import.mixin` from a custom model that owns a staging table workflow. See `odoo_addon/odoo_batch_import_mixin/README.md`.

## Benchmarking

The benchmark utilities can compare row preparation, dry-run payload generation, and PostgreSQL insertion strategies when a database is configured. See `docs/benchmarking-guide.md` for fair comparison notes.

## Safety notes

- Prefer staging tables over direct writes to Odoo core tables.
- Test against a staging database first.
- Back up the target database before any real import.
- Make imports idempotent with external references.
- Keep credentials in environment variables or ignored config files.
- Use transactions and roll back on failures.

## Tests

```bash
pytest
```

Tests do not require PostgreSQL or Odoo.

## GitHub push

```bash
git init
git add .
git commit -m "initial commit"
git branch -M main
git remote add origin https://github.com/gharisj3/odoo-batch-import-toolkit.git
git push -u origin main
```

If GitHub CLI is authenticated:

```bash
gh repo create gharisj3/odoo-batch-import-toolkit --public --source=. --remote=origin --push
```

## License

MIT. See `LICENSE`.
