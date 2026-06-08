"""Reusable Odoo mixin for staged import processing."""

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class OdooBatchImportMixin(models.AbstractModel):
    _name = "odoo.batch.import.mixin"
    _description = "Batch Import Mixin"

    batch_import_batch_size = fields.Integer(default=1000)

    def _batch_import_prepare_values(self, row):
        """Map a staging row to ORM create/write values.

        Inheriting models should override this method.
        """
        return dict(row)

    def _batch_import_validate_row(self, row):
        """Validate one staging row before ORM processing."""
        if not row:
            raise ValidationError("Empty staging row cannot be processed.")
        return True

    @api.model
    def _batch_import_create_records(self, rows, batch_size=1000):
        created = self.env[self._name].browse()
        buffer = []
        for row in rows:
            self._batch_import_validate_row(row)
            buffer.append(self._batch_import_prepare_values(row))
            if len(buffer) >= batch_size:
                created |= self.create(buffer)
                buffer = []
        if buffer:
            created |= self.create(buffer)
        return created

    @api.model
    def _batch_import_update_status(self, staging_records, status, message=None):
        values = {"status": status}
        if message is not None:
            values["error_message"] = message
        if status in {"done", "error"}:
            values["processed_at"] = fields.Datetime.now()
        staging_records.write(values)

    def action_process_staging_batch(self):
        """Entry point for custom models.

        Override in the concrete model because each implementation owns a
        different staging model/table and target model mapping.
        """
        raise NotImplementedError("Implement action_process_staging_batch in the concrete import model.")
