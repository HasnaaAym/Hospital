from odoo import models,fields

class HmsDepartment(models.Model):
    _name="hms.department"
    _description = 'Department Information'

    name = fields.Char()
    capacity = fields.Integer()
    is_opened = fields.Boolean()
    patient_id = fields.One2many("hms.patient","department_id")