# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, api
import openerp.addons.decimal_precision as dp


class HRSettingsConf(models.TransientModel):

    _inherit = 'hr.payroll.config.settings'

    rent_company_id = fields.Many2one('res.company', string='Company',
                                      required=True)
    first_limit = fields.Float(
        string='First Limit', digits=dp.get_precision('Payroll'),
        default=0.0)
    second_limit = fields.Float(
        string='Second Limit', digits=dp.get_precision('Payroll'),
        default=0.0)
    amount_per_child = fields.Float(
        string='Amount per Child', digits=dp.get_precision('Payroll'),
        default=0.0)
    amount_per_spouse = fields.Float(
        string='Amount per spouse', digits=dp.get_precision('Payroll'),
        default=0.0)

    """Override onchange_company_id to update rent limits """
    @api.onchange('rent_company_id')
    def onchange_rent_company_id(self, rent_company_id):
        if rent_company_id:
            company = self.env['res.company'].browse(rent_company_id)
            self.first_limit = company.first_limit
            self.second_limit = company.second_limit,
            self.amount_per_child = company.amount_per_child,
            self.amount_per_spouse = company.amount_per_spouse,
        else:
            self.first_limit = 0.0
            self.second_limit = 0.0
            self.amount_per_child = 0.0
            self.amount_per_spouse = 0.0

    """Get the default company for the module"""
    @api.model
    def get_default_rent_company_id(self):
        return {'rent_company_id': self._company_default_get()}

    """Get the default first_limit"""
    @api.model
    def get_first_limit(self):
        company = self._company_default_get()
        return {'first_limit': company.first_limit}

    """Set the default first_limit"""
    @api.model
    def set_first_limit(self):
        self.rent_company_id.write({'first_limit': self.first_limit})

    """Get the default second_limit"""
    @api.model
    def get_second_limit(self):
        company = self._company_default_get()
        return {'second_limit': company.second_limit}

    """Set the default second_limit in the selected company"""
    @api.model
    def set_second_limit(self):
        self.rent_company_id.write({'second_limit': self.second_limit})

    """Get the default amount_per_child"""
    @api.model
    def get_amount_per_child(self, cr, uid, fields, context=None):
        company = self._company_default_get()
        return {'amount_per_child': company.amount_per_child}

    """Set the default amount_per_child in the selected company"""
    @api.model
    def set_amount_per_child(self):
        self.rent_company_id.write({'amount_per_child': self.amount_per_child})

    """Get the default amount_per_spouse"""
    @api.model
    def get_amount_per_spouse(self):
        company = self._company_default_get()
        return {'amount_per_spouse': company.amount_per_spouse}

    """Set the default amount_per_spouse in the selected company"""
    @api.model
    def set_amount_per_spouse(self):
        self.rent_company_id.write(
            {'amount_per_spouse': self.amount_per_spouse})
