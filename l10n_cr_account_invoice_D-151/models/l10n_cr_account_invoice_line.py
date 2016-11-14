# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import fields, osv

class accountInvoicelineD151(osv.Model):

    _inherit = 'account.invoice.line'

    def _get_type_invoice(self, cr, uid, context=None):
        if context is None:
            context = {}
        return context.get('type')

    def _get_type_invoice_line(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for line in self.browse(cr, uid, ids,context=context):
            res[line.id] = line.invoice_id.type
        return res

    #This field add category D-151 to invoice line.
    _columns = {
        'd_151_type':fields.selection([('V','Goods and services sales'),
                                       ('C','Goods and services purchases'),
                                       ('A','Rent'),
                                       ('SP','Profesional services'),
                                       ('M','Commissions'),
                                       ('I','Interest')], string='D-151 Type'),
        'type_invoice': fields.function(_get_type_invoice_line, type='char', string='Invoice type', size=64)
    }

    #Get the type of invoice for category D-151    
    _defaults = {
        'type_invoice': _get_type_invoice,
    }
