from __future__ import annotations

import argparse
import csv
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate safe sample partner CSV data.")
    parser.add_argument("--rows", type=int, default=10000)
    parser.add_argument("--output", default="examples/generated_partners_10k.csv")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["external_ref", "name", "email", "phone", "company_name"])
        writer.writeheader()
        for number in range(1, args.rows + 1):
            writer.writerow(
                {
                    "external_ref": f"PARTNER-{number:05d}",
                    "name": f"Sample Partner {number}",
                    "email": f"partner{number}@example.com",
                    "phone": f"+100000{number:05d}",
                    "company_name": "Example Company",
                }
            )
    print(f"Wrote {args.rows} rows to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
