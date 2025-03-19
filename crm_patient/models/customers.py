from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CrmCustomers(models.Model):
    _inherit = "res.partner"
    related_patient_id = fields.Many2one("hms.patient", string="patient_id")
    email = fields.Char(string="email")
    website = fields.Char(string="website")
    tax_id = fields.Char(string="tax_id")

    @api.constrains("email")
    def _check_email(self):
        for record in self:
            patient = self.env['hms.patient'].search([('email', '=', record.email)])
            if patient:
                raise ValidationError("email already exists")

    @api.model
    def unlink(self):
        for record in self:
            if record.related_patient_id:
                raise ValidationError("you cannot delete this patient")
        return super().unlink()

    @api.constrains('tax_id')
    def _check_tax_id(self):
        for record in self:
            if not record.tax_id:
                raise ValidationError("Tax ID is required")
