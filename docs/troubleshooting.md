# Troubleshooting

## PostgreSQL connection refused

Check `POSTGRES_HOST`, `POSTGRES_PORT`, firewall rules, and whether PostgreSQL is running.

## Authentication failed

Verify `POSTGRES_USER`, `POSTGRES_PASSWORD`, and database permissions. Do not put real passwords in Git.

## Invalid CSV headers

Run `validate` and compare the required headers with the CSV header row.

## Duplicate key violation

Check `external_ref` uniqueness and any unique indexes on staging or target tables.

## Permission denied for table

Grant the database user insert/select/update rights on the staging table.

## Odoo computed fields not updating

Direct SQL bypasses Odoo compute logic. Load into staging and process through ORM.

## Direct SQL data not visible correctly in Odoo

The row may be missing required Odoo metadata, company fields, relational links, or computed values. Prefer ORM processing.

## Encoding issues

Save CSV files as UTF-8. The loader supports UTF-8 with BOM.

## Transaction rollback

Failures in non-dry-run insert mode roll back the connection before the error is raised.
