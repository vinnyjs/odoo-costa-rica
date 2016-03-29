# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Addons modules by CLEARCORP S.A.
#    Copyright (C) 2009-TODAY CLEARCORP S.A. (<http://clearcorp.co.cr>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api


class PayrollReportEmployee(models.TransientModel):
    """Payroll Report Employee"""

    _name = 'l10n.cr.hr.payroll.by.periods.employee'
    _description = __doc__

    company_id = fields.Many2one('res.company', string='Company')
    format = fields.Selection(
        [('qweb-pdf', 'PDF'), ('qweb-xls', 'XLS')],
        string='Format', default='qweb-pdf')
    filter = fields.Selection(
        [('date', 'Date'), ('period', 'Period')],
        string='Filter', default='period')
    period_from = fields.Many2one('account.period', string='Start Period')
    period_to = fields.Many2one('account.period', string='End Period')
    date_from = fields.Date('Start Date')
    date_to = fields.Date('End Date')

    _defaults = {
        'company_id': lambda self, cr, uid, context:
            self.pool.get('res.users').browse(
                cr, uid, uid,
                context=context).company_id.id,
    }

    @api.multi
    def print_report(self):
        if self.filter == 'period':
            date_from = self.env['account.period'].search(
                [('id', '=', self.period_from.id)])[0].date_start
            date_to = self.env['account.period'].search(
                [('id', '=', self.period_to.id)])[0].date_stop
        else:
            date_from = self.date_from
            date_to = self.date_to
        data = {
            'period_from': date_from,
            'period_to': date_to,
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

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: