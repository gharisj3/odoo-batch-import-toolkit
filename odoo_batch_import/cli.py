"""Command line interface for the Odoo batch import toolkit."""

from __future__ import annotations

import argparse
import sys

from .batch_insert import batch_insert
from .benchmark import run_dry_run_benchmark
from .config import load_config
from .csv_loader import stream_csv_rows, validate_csv_file
from .db import connect
from .explain import explain_analyze, read_sql_file
from .reporting import print_summary
from .validators import validate_rows


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="odoo-batch-import", description="Validate, stage, and benchmark Odoo CSV imports.")
    parser.add_argument("--env-file", default=".env", help="Path to local env file. Defaults to .env.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Validate CSV headers and common row values.")
    validate.add_argument("--file", required=True)
    validate.add_argument("--required", nargs="*", default=[])

    import_cmd = subparsers.add_parser("import", help="Insert CSV rows into a PostgreSQL table.")
    import_cmd.add_argument("--file", required=True)
    import_cmd.add_argument("--table", required=True)
    import_cmd.add_argument("--batch-size", type=int)
    import_cmd.add_argument("--dry-run", action="store_true")
    import_cmd.add_argument("--execute", action="store_true", help="Run against PostgreSQL instead of dry-run.")
    import_cmd.add_argument("--allow-direct-table-write", action="store_true")

    benchmark = subparsers.add_parser("benchmark", help="Run a benchmark report.")
    benchmark.add_argument("--file", required=True)
    benchmark.add_argument("--table", required=True)
    benchmark.add_argument("--batch-size", type=int)
    benchmark.add_argument("--dry-run", action="store_true")

    explain = subparsers.add_parser("explain", help="Run EXPLAIN ANALYZE for SQL statements.")
    explain.add_argument("--sql", required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = load_config(env_file=args.env_file)

    if args.command == "validate":
        header_result = validate_csv_file(args.file, required_headers=args.required)
        if not header_result.ok:
            for error in header_result.errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        row_result = validate_rows(stream_csv_rows(args.file, required_headers=args.required), required=args.required)
        if not row_result.ok:
            for error in row_result.errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1
        print("CSV validation passed.")
        return 0

    if args.command == "import":
        dry_run = True
        if args.execute:
            dry_run = False
        elif args.dry_run:
            dry_run = True
        else:
            dry_run = config.import_defaults.dry_run
        batch_size = args.batch_size or config.import_defaults.batch_size
        rows = stream_csv_rows(args.file)
        if dry_run:
            summary = batch_insert(None, args.table, rows, batch_size=batch_size, dry_run=True, allow_direct_table_write=args.allow_direct_table_write)
        else:
            with connect(config.postgres) as conn:
                summary = batch_insert(conn, args.table, rows, batch_size=batch_size, dry_run=False, allow_direct_table_write=args.allow_direct_table_write)
        print_summary(summary)
        return 0

    if args.command == "benchmark":
        batch_size = args.batch_size or config.import_defaults.batch_size
        print(run_dry_run_benchmark(args.file, args.table, batch_size=batch_size))
        return 0

    if args.command == "explain":
        sql = read_sql_file(args.sql)
        with connect(config.postgres) as conn:
            for plan in explain_analyze(conn, sql):
                print(plan)
                print()
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
