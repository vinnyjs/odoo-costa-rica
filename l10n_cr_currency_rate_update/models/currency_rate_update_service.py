# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields
from openerp.tools.translate import _


class CurrencyRateUpdateService(models.Model):

    _inherit = 'currency.rate.update.service'

    interval_type = fields.Selection(
        selection_add=[('hours', 'Hour(s)'),
                       ('days', 'Day(s)'),
                       ('weeks', 'Week(s)'),
                       ('months', 'Month(s)')],
        string='Currency update frequency', default='days')

    _sql_constraints = [(
        'curr_service_unique',
        'check (1 = 1)',
        _('You can use a service only one time per company'))]
