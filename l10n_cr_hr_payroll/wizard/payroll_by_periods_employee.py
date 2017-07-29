# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class PayrollReportEmployee(models.TransientModel):
    """Payroll Report Employee"""

    _name = 'l10n.cr.hr.payroll.by.periods.employee'
    _description = __doc__

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)
    format = fields.Selection(
        [('qweb-pdf', 'PDF'), ('qweb-xls', 'XLS')],
        string='Format', default='qweb-pdf')
    filter = fields.Selection(
        [('date', 'Date')],
        string='Filter', default='date')
    date_from = fields.Date('Start Date', required=True)
    date_to = fields.Date('End Date', required=True)

    @api.multi
    def print_report(self):
        data = {
            'period_from': self.date_from,
            'period_to': self.date_to,
        }
        if self.format == 'qweb-pdf':
            res = self.env['report'].get_action(
                self.company_id,
                'l10n_cr_hr_payroll.report_payroll_periods_employee',
                data=data)
        else:
            res = self.env['report'].get_action(
                self.company_id,
                'l10n_cr_hr_payroll.report_payroll_xls_employee',
                data=data)
        return res
