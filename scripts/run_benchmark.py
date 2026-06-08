from __future__ import annotations

import argparse

from odoo_batch_import.benchmark import run_dry_run_benchmark


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a dry-run benchmark report.")
    parser.add_argument("--file", default="examples/partners_10k_sample.csv")
    parser.add_argument("--table", default="staging_partner_import")
    parser.add_argument("--batch-size", type=int, default=1000)
    args = parser.parse_args()
    print(run_dry_run_benchmark(args.file, args.table, batch_size=args.batch_size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
