# Odoo Batch Import Benchmark

| Scenario | Records | Batch size | Runtime | Rows/sec | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| dry-run payload preparation | 10000 | 1000 | 0.0450s | 222222.22 | No database connection used. |
| executemany staging insert | 10000 | 1000 | 1.2500s | 8000.00 | Example only; measure on your database. |

## Recommendation

Use raw PostgreSQL for validated staging-table loading, then process staged rows through Odoo ORM in controlled batches.
