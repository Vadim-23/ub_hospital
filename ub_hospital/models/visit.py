from odoo import fields, models, api, _
from odoo.exceptions import UserError


class UBHospitalVisit(models.Model):
    _name = 'ub.hospital.visit'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Description'

    name = fields.Char(compute='_compute_name', )
    date_start = fields.Datetime(default=fields.Datetime.now(), required=True)
    doctor_id = fields.Many2one('ub.hospital.doctor', )
    patient_id = fields.Many2one('ub.hospital.patient', required=True)
    disease_id = fields.Many2one('ub.hospital.disease', )
    active = fields.Boolean(default=True)
    diagnosis = fields.Text()
    date_checkup = fields.Datetime()
    state = fields.Selection([('draft', 'Draft'),
                              ('checkup', 'Checkup'),
                              ('done', 'Done'),
                              ('cancel', 'Cancel'),
                              ],
                             default='draft',
                             required=True)
    stage_sort = fields.Selection([('1', 'Draft'),
                                   ('2', 'Checkup'),
                                   ('3', 'Done'),
                                   ('4', 'Cancel'), ],
                                  compute='_compute_stage_sort',
                                  store=True)
    state_color = fields.Char(compute='_compute_state_color')

    @api.model
    def create(self, vals):
        if vals.get('date_start'):
            date_start = fields.Datetime.from_string(vals.get('date_start'))
            if date_start < fields.Datetime.now():
                raise UserError(_('You can not create visit for past date'))
        return super(UBHospitalVisit, self).create(vals)

    @api.depends('state')
    def _compute_state_color(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state_color = 'grey'
            elif rec.state == 'checkup':
                rec.state_color = 'blue'
            elif rec.state == 'done':
                rec.state_color = 'green'
            elif rec.state == 'cancel':
                rec.state_color = 'red'

    @api.depends('date_start', 'doctor_id', 'patient_id')
    def _compute_name(self):
        for record in self:
            record.name = 'Patient: %s, Doctor: %s, Date: %s' % (
                record.patient_id.name,
                record.doctor_id.name,
                record.date_start)
        self._compute_stage_sort()

    def _compute_stage_sort(self):
        for record in self:
            if record.state == 'draft':
                record.stage_sort = '1'
            elif record.state == 'checkup':
                record.stage_sort = '2'
            elif record.state == 'done':
                record.stage_sort = '3'
            elif record.state == 'cancel':
                record.stage_sort = '4'

    @api.constrains('date_start', 'doctor_id', 'patient_id')
    def _check_unique_visit(self):
        for record in self:
            visits = self.env['ub.hospital.visit'].search([
                ('id', '!=', record.id),
                ('doctor_id', '=', record.doctor_id.id),
                ('date_start', '=', record.date_start),
            ])
            if visits:
                raise models.ValidationError(_(
                    'A visit with the same doctor '
                    'and start date and time already exists.'))
            visits = self.env['ub.hospital.visit'].search([
                ('id', '!=', record.id),
                ('patient_id', '=', record.patient_id.id),
                ('date_start', '=', record.date_start),
            ])
            if visits:
                raise models.ValidationError(_(
                    'A visit with the same patient '
                    'and start date and time already exists.'))
        self._compute_stage_sort()

    def action_checkup(self):
        if not self.doctor_id:
            raise UserError(_("Please select a "
                            "doctor before marking this visit as done."))
        self.state = 'checkup'
        self.date_checkup = fields.Datetime.now()
        self.patient_id.doctor_id = self.doctor_id.id

    def action_done(self):
        if not self.date_checkup or not self.diagnosis:
            raise UserError(_("Please fill in the required"
                            " fields before marking this visit as done."))
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'checkup' and \
                (not self.date_checkup or not self.diagnosis):
            raise UserError(_("Please fill in the required"
                            " fields before marking this visit as done."))

    def write(self, vals):
        if vals.get('date_start'):
            if vals['date_start'] < fields.Datetime.now():
                raise UserError(_("Cannot change date to past"))
        if any(visit.state == 'done' for visit in self):
            for visit in self:
                if 'diagnosis' in vals and visit.diagnosis:
                    raise UserError(_("Cannot change diagnosis "
                                      "of completed visit"))
                if 'date_checkup' in vals and visit.date_checkup:
                    raise UserError(_("Cannot change date "
                                      "of completed visit"))
                if 'doctor_id' in vals and visit.doctor_id:
                    raise UserError(_("Cannot change doctor "
                                      "of completed visit"))
                if 'patient_id' in vals and visit.patient_id:
                    raise UserError(_("Cannot change patient"
                                      " of completed visit"))
        return super(UBHospitalVisit, self).write(vals)

    def unlink(self):
        for record in self:
            if record.diagnosis:
                raise UserError(_("You cannot delete or archive "
                                "a visit with a diagnosis."))
        return super(UBHospitalVisit, self).unlink()
