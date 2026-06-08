from __future__ import annotations

import argparse
from pathlib import Path

from odoo_batch_import.benchmark import run_dry_run_benchmark


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a markdown comparison report for import strategies.")
    parser.add_argument("--file", default="examples/partners_10k_sample.csv")
    parser.add_argument("--table", default="staging_partner_import")
    parser.add_argument("--batch-size", type=int, default=1000)
    parser.add_argument("--output", default="examples/benchmark_result_generated.md")
    args = parser.parse_args()

    report = run_dry_run_benchmark(args.file, args.table, batch_size=args.batch_size)
    report += "\n## Strategy notes\n\n"
    report += "- Single-row insert loops are simple but usually slow because each row pays round-trip overhead.\n"
    report += "- `executemany` improves batching while keeping parameterized SQL.\n"
    report += "- `execute_values` can be faster with psycopg2, but still needs identifier validation and transaction handling.\n"
    report += "- `COPY` can be very fast for staging tables when input is trusted and validated.\n"
    report += "- Staging-table insert followed by Odoo ORM processing is the recommended default.\n"

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
