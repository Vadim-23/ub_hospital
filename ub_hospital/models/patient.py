from odoo import fields, models


class UBHospitalPatient(models.Model):
    _name = 'ub.hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Description'

    name = fields.Char(required=True)
    doctor_id = fields.Many2one('ub.hospital.doctor', )
    active = fields.Boolean(default=True)
    image = fields.Binary(string="Patient Image")
    phone = fields.Char(reqired=True)
