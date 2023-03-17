from odoo import fields, models


class UBHospitalDoctor(models.Model):
    _name = 'ub.hospital.doctor'
    _description = 'Description'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True)
    specialization = fields.Char(default='General')
    patient_ids = fields.One2many('ub.hospital.patient', 'doctor_id', )
    image = fields.Binary(string="Doctor Image", attachment=True,
                          help="This field holds the image used"
                               " as avatar for this doctor, "
                               "limited to 1024x1024px")
    active = fields.Boolean(default=True)
