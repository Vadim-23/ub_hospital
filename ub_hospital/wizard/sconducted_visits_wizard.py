from datetime import timedelta

from odoo import fields, models


class ConductedVisitsWizard(models.TransientModel):
    _name = 'conducted.visits.wizard'
    _description = 'Conducted Visits Wizard'

    doctor_id = fields.Many2one('ub.hospital.doctor',
                                string='Doctor',
                                required=True)
    patient_id = fields.Many2one('ub.hospital.patient',
                                 string='Patient',
                                 required=True)
    date_from = fields.Date(required=True,
                            default=fields.Date.today())
    date_to = fields.Date(required=True,
                          default=fields.Date.today() + timedelta(days=30))

    def action_generate_report(self):
        # get all visits of the patient
        visits = self.env['ub.hospital.visit'].search([
            ('patient_id', '=', self.patient_id.id),
            ('date_start', '>=', self.date_from),
            ('date_start', '<=', self.date_to),
            ('state', '=', 'done'),
            ('doctor_id', '=', self.doctor_id.id)
        ])
        docs = [
            {
                'date_checkup': visit.date_checkup,
                'doctor_name': visit.doctor_id.name,
                'diagnosis': visit.diagnosis,
            } for visit in visits
        ]
        data = {
            'patient_name': self.patient_id.name,
            'patient_phone': self.patient_id.phone,
            'docs': docs,
            'data': docs,
            'count': len(visits),
            'start_date': self.date_from,
            'end_date': self.date_to,
        }
        self_doctor = self.doctor_id
        report = self.env.ref(
            'ub_hospital.report_conducted_visit').report_action(
            self_doctor, data=data)
        return report
