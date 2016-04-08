# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api
from openerp.tools.translate import _


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    @api.one
    def copy_data(self, default=None):
        if default is None:
            default = {}
        name = self.read(['name'])['name']
        default = default.copy()
        default.update({'name': name + _(' (Copy)')})
        default.update({'identification_id': False})
        return super(HREmployee, self).copy_data(default=default)

    _sql_constraints = [
        ('identification_unique',
         'UNIQUE(identification_id)',
         'The Nº Identification already exist for other employee')
    ]
