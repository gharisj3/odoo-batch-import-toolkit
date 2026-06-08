CREATE TABLE IF NOT EXISTS staging_partner_import (
    id BIGSERIAL PRIMARY KEY,
    external_ref TEXT,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    company_name TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    error_message TEXT,
    payload_json JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    processed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_staging_partner_import_status
    ON staging_partner_import (status);

CREATE UNIQUE INDEX IF NOT EXISTS idx_staging_partner_import_external_ref
    ON staging_partner_import (external_ref)
    WHERE external_ref IS NOT NULL;

CREATE TABLE IF NOT EXISTS staging_product_import (
    id BIGSERIAL PRIMARY KEY,
    external_ref TEXT,
    name TEXT NOT NULL,
    default_code TEXT,
    list_price NUMERIC,
    type TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    error_message TEXT,
    payload_json JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    processed_at TIMESTAMPTZ
);
