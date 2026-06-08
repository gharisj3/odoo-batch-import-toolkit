# Odoo ORM vs Raw SQL

| Approach | Strengths | Risks | Best use |
| --- | --- | --- | --- |
| Odoo ORM `create`/`write` | Runs business logic, constraints, computed fields, tracking, and access rules | Slower for very large imports | Final record creation and updates |
| XML-RPC/JSON-RPC import | Remote-friendly and uses ORM | Network overhead and slower throughput | External integrations and small to medium imports |
| Raw PostgreSQL direct insert | Fast | Bypasses Odoo behavior and can corrupt business data | Advanced maintenance only after review |
| Raw PostgreSQL staging plus ORM | Fast loading with safer final processing | Requires staging schema and processing code | Recommended default for high-volume imports |
