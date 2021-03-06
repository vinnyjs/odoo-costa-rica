# -*- encoding: utf-8 -*-
##############################################################################
#
#    l10n_cr_base.py
#    l10n_cr_base
#    First author: Carlos Vásquez <carlos.vasquez@clearcorp.co.cr> (ClearCorp S.A.)
#    Copyright (c) 2010-TODAY ClearCorp S.A. (http://clearcorp.co.cr). All rights reserved.
#    
#    Redistribution and use in source and binary forms, with or without modification, are
#    permitted provided that the following conditions are met:
#    
#       1. Redistributions of source code must retain the above copyright notice, this list of
#          conditions and the following disclaimer.
#    
#       2. Redistributions in binary form must reproduce the above copyright notice, this list
#          of conditions and the following disclaimer in the documentation and/or other materials
#          provided with the distribution.
#    
#    THIS SOFTWARE IS PROVIDED BY <COPYRIGHT HOLDER> ``AS IS'' AND ANY EXPRESS OR IMPLIED
#    WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
#    FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> OR
#    CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#    ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#    ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#    
#    The views and conclusions contained in the software and documentation are those of the
#    authors and should not be interpreted as representing official policies, either expressed
#    or implied, of ClearCorp S.A..
#    
##############################################################################

from osv import osv,fields
import pooler
import time
from base.res.res_partner import _lang_get

class res_partner(osv.osv):
    '''
    Inherits res.partner to add lang default value
    '''
    _inherit = 'res.partner'
    _columns = {
        'lang': fields.selection(_lang_get, 'Language', required=True, help="If the selected language is loaded in the system, all documents related to this partner will be printed in this language. If not, it will be english."),
    }
    _defaults = {
        'lang': lambda *a: 'es_CR',
        'title': lambda self,cr,uid,ctx={}: self.pool.get('res.partner.title').search(cr, uid, [('shortcut','=','Corp.')])[0],
        'date': lambda *args: time.strftime('%Y-%m-%d'),
    }
    
    def lang_es_install(self, cr, uid):
        lang = 'es_CR'
        modobj = pooler.get_pool(cr.dbname).get('ir.module.module')
        mids = modobj.search(cr, uid, [('state', '=', 'installed')])
        modobj.update_translations(cr, uid, mids, lang)
        return {}

class res_country_state_canton(osv.osv):
     _name = 'res.country.state.canton'
     _description = 'Canton'
     _columns = {
        'state_id'   : fields.many2one('res.country.state','State',required=True),
        'name'       : fields.char('Name', size=64, required=True),
        'code'       : fields.char('Code', size=2, help = 'Official code: XX', required=True),
     }

class res_country_state_canton_district(osv.osv):
     _name = 'res.country.state.canton.district'
     _description = 'District'
     _columns = {
        'canton_id'  : fields.many2one('res.country.state.canton','Canton',required=True),
        'name'       : fields.char('Name', size=64, required=True),
        'code'       : fields.char('Code', size=2,help = 'Official code: XX', required=True),
     }

class res_partner_address(osv.osv):
    '''
    Inherits res.partner.address to add country and state default values
    '''
    _inherit = 'res.partner.address'
    _columns = {
            'canton_id'   : fields.many2one('res.country.state.canton', 'Canton'),
            'district_id' : fields.many2one('res.country.state.canton.district', 'Canton'),
    }

    _defaults = {
        'country_id': lambda self,cr,uid,ctx={}: self.pool.get('res.country').search(cr, uid, [('name','=','Costa Rica')])[0],
        'state_id': lambda self,cr,uid,ctx={}: self.pool.get('res.country.state').search(cr, uid, [('country_id','=','Costa Rica'),('name','=','San José')])[0],
    }

class res_users(osv.osv):
    '''
    Inherits res.users to add lang and tz default values
    '''
    _inherit = 'res.users'
    _defaults = {
        'context_lang': lambda *a: 'es_CR',
        'context_tz': lambda *a: 'America/Costa_Rica',
    }
