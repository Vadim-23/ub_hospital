from datetime import timedelta

from odoo import fields, models


class VisitPatientWizard(models.TransientModel):
    _name = 'visit.patient.wizard'
    _description = 'Description'

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
            ('state', '=', 'done')
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
        self_patient = self.patient_id
        report = self.env.ref(
            'ub_hospital.report_patient_visit').report_action(
            self_patient, data=data)
        return report
