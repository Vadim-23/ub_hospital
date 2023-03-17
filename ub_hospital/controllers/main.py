import json
from datetime import datetime

from odoo import http
from odoo.http import request


class VisitController(http.Controller):

    @http.route('/api/create_visit', type='json', auth='public', website=False,
                csrf=False, methods=["GET", "POST"])
    def create_visit(self):
        kw = request.jsonrequest
        if kw.get('phone') and kw.get('date'):
            patient = self.get_or_create_patient(kw.get('phone'))
            date_start = datetime.strptime(kw.get('date'), '%d.%m.%Y')
            request.env['ub.hospital.visit'].sudo().create({
                'patient_id': patient.id,
                'date_start': date_start,
                'state': 'draft',
            })
            return json.dumps({'status': 'ok',
                               'message': 'Visit created successfully',
                               'patient': patient.name,
                               'date': kw.get('date')})
        return json.dumps({'status': 'error',
                           'message': 'Phone or date is missing'})

    def get_or_create_patient(self, phone):
        # search the patient
        # if not found, create a new patient
        # return the patient
        patient = request.env['ub.hospital.patient'].sudo().search(
            [('phone', '=', phone)])
        if not patient:
            patient = request.env['ub.hospital.patient'].sudo().create({
                'name': phone,
                'phone': phone,
            })
        return patient
