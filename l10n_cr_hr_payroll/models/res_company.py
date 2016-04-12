# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class resCompanyInherit(osv.Model):

    _inherit = 'res.company'

    _columns = {
        'first_limit': fields.float('First Limit', digits_compute=dp.get_precision('Payroll')),
        'second_limit':fields.float('Second Limit', digits_compute=dp.get_precision('Payroll')), 
        'amount_per_child': fields.float('Amount per Child', digits_compute=dp.get_precision('Payroll')),
        'amount_per_spouse': fields.float('Amount per spouse', digits_compute=dp.get_precision('Payroll')),
        
    }