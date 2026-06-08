# Benchmarking Guide

Generate sample data:

```bash
python scripts/generate_sample_csv.py --rows 10000 --output examples/generated_partners_10k.csv
```

Run dry-run benchmark:

```bash
python scripts/run_benchmark.py --file examples/generated_partners_10k.csv --table staging_partner_import
```

Create a markdown comparison:

```bash
python scripts/explain_analyze_compare.py --file examples/generated_partners_10k.csv --output examples/benchmark_result_generated.md
```

Rows per second is useful only when comparing similar hardware, indexes, database settings, CSV shape, and transaction size. Larger batches usually reduce round trips, but very large batches can increase memory usage and lock duration.

Use `EXPLAIN ANALYZE` to inspect scans, index usage, row estimates, timing, and buffer activity. Compare results after warming caches and repeat each scenario several times.
