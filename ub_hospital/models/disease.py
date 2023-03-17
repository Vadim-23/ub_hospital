from odoo import fields, models


class UBHospitalDisease(models.Model):
    _name = 'ub.hospital.disease'
    _description = 'Description'

    name = fields.Char(required=True)
