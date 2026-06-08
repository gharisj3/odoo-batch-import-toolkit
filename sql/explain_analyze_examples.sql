SELECT count(*) FROM staging_partner_import WHERE status = 'pending';

SELECT external_ref, count(*)
FROM staging_partner_import
WHERE external_ref IS NOT NULL
GROUP BY external_ref
HAVING count(*) > 1;

SELECT id, name, email
FROM staging_partner_import
WHERE status = 'pending'
ORDER BY id
LIMIT 1000;

SELECT count(*)
FROM staging_partner_import
WHERE name IS NULL OR name = '';

INSERT INTO staging_partner_import (external_ref, name, email, phone, company_name)
VALUES ('BENCH-00001', 'Benchmark Partner', 'benchmark@example.com', '+10000000000', 'Example Company');
