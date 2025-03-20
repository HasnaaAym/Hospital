import re
from email.policy import default

from Tools.scripts.objgraph import store

from odoo import models, fields, api
from odoo.api import constrains
from odoo.exceptions import ValidationError
from odoo.tools import datetime


class HmsPatient(models.Model):
    _name = "hms.patient"
    _description = 'Patient Information'

    first_name = fields.Char()
    last_name = fields.Char()
    name = fields.Char(compute='_compute_name',store=True)
    email = fields.Char()
    birth_day = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection(
        [('A', 'A'),
         ('B', 'B'),
         ('AB', 'AB'),
         ('O', 'O'), ])
    state = fields.Selection(
        [("U", "Undetermined"),
         ("G", "Good"),
         ("F", "Fair"),
         ("S", "Serious")]
    ,default='G')
    pcr = fields.Boolean()
    image = fields.Binary()
    address = fields.Text()
    age = fields.Integer(compute="calc_age", store=True)
    department_id = fields.Many2one("hms.department")
    department_capacity = fields.Integer(related="department_id.capacity")
    doctor_ids = fields.Many2many("hms.doctor")
    patient_log_history_ids = fields.One2many("patient.log.history", "patient_id")

    def change_state(self, new_state):
        self.state = new_state

        self.env["patient.log.history"].create({
            'patient_id': self.id,
            'created_by': self.env.user.id,
            'date': fields.Datetime.now(),
            'description': f"state change to {new_state}"
        })

    def set_state_undetermined(self):
        self.change_state("U")

    def set_state_good(self):
        self.change_state("G")

    def set_state_fair(self):
        self.change_state("F")

    def set_state_serious(self):
        self.change_state("S")

    @api.onchange("age")
    def _on_change_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'PCR checked',
                    'message': 'PCR has been automatically checked'
                }
            }
        else:
            self.pcr = False

    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)', 'Email address must be unique!')
    ]

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if not record.email:
                raise ValidationError("Email is required")
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if record.email and not re.match(email_regex, record.email):
                raise ValidationError("Invalid email address")

    @api.depends("birth_day")
    def calc_age(self):
        for record in self:
            if record.birth_day:
                birth_day = record.birth_day
                record.age = datetime.today().year - birth_day.year
            else:
                record.age = 0

    @api.depends('first_name','last_name')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.first_name} {record.last_name}"

class PatientLogHistory(models.Model):
    _name = "patient.log.history"
    _description = 'Patient Information'


    patient_id = fields.Many2one("hms.patient")
    created_by = fields.Many2one("res.users", default=lambda self: self.env.user)
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    description = fields.Text()
