# Odoo Batch Import Mixin

This addon provides the abstract model `odoo.batch.import.mixin` for processing rows that were first loaded into PostgreSQL staging tables.

## Install

1. Copy `odoo_batch_import_mixin` into an Odoo addons path.
2. Restart Odoo.
3. Update the apps list.
4. Install `Odoo Batch Import Mixin`.

## Why staging first

Raw SQL into core Odoo tables can bypass ORM validation, computed fields, access logic, mail tracking, automated actions, and module-specific business rules. A safer pattern is:

```text
CSV -> validation -> PostgreSQL staging table -> Odoo ORM processing
```

## Example inheritance

```python
class PartnerImportWizard(models.TransientModel):
    _name = "partner.import.wizard"
    _inherit = ["odoo.batch.import.mixin"]

    def _batch_import_prepare_values(self, row):
        return {
            "name": row.name,
            "email": row.email,
            "phone": row.phone,
        }

    def action_process_staging_batch(self):
        rows = self.env["staging.partner.import"].search([("status", "=", "pending")], limit=1000)
        records = self.env["res.partner"]._batch_import_create_records(rows, batch_size=1000)
        self._batch_import_update_status(rows, "done")
        return records
```

Adapt the staging model/table and target model to your module.
