# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from xml.dom.minidom import parseString
from openerp.addons.currency_rate_update import CurrencyGetterInterface
from datetime import datetime
from openerp.exceptions import except_orm


_logger = logging.getLogger(__name__)


class BccrGetter(CurrencyGetterInterface):

    code = 'BCCR'
    name = 'Central Bank of Costa Rica'
    log_info = " "

    def get_url(self, url):
        """Return a string of a get url query"""
        try:
            import urllib
            objfile = urllib.urlopen(url)
            rawfile = objfile.read()
            objfile.close()
            return rawfile
        except ImportError:
            raise except_orm(
                'Error ! Unable to import urllib !')
        except IOError:
            raise except_orm(
                'Error ! Web Service does not exist !')

    def get_updated_currency(
            self, currency_array, main_currency, max_delta_days, code_rate=''):
        """implementation of abstract method of Curreny_getter_interface"""

        today = datetime.today()
        today_str = today.strftime('%d/%m/%Y')
        url1 = 'http://indicadoreseconomicos.bccr.fi.cr/' + \
            'indicadoreseconomicos/WebServices/wsIndicadoresEconomicos' + \
            '.asmx/ObtenerIndicadoresEconomicos?tcNombre=ClearCorp' + \
            '&tnSubNiveles=N&tcFechaFinal=' + today_str + '&tcFechaInicio='
        url2 = '&tcIndicador='

        self.updated_currency = {}

        for curr in currency_array:
            self.updated_currency[curr] = {}
            last_rate_date = today_str
            url = url1 + last_rate_date + url2

            # Build the url and log it
            url = url + code_rate
            _logger.info('URL %s' % url)
            rawstring = self.get_url(url)
            dom = parseString(rawstring)
            nodes = dom.getElementsByTagName('INGC011_CAT_INDICADORECONOMIC')
            for node in nodes:
                num_valor = node.getElementsByTagName('NUM_VALOR')
                if len(num_valor):
                    rate = num_valor[0].firstChild.data
                else:
                    continue
                des_fecha = node.getElementsByTagName('DES_FECHA')
                if not len(des_fecha):
                    continue
                if float(rate) > 0.0:
                    self.updated_currency[curr] = rate
                    _logger.debug("Rate retrieved : %s = %s %s" %
                                  (main_currency, rate, curr))
        _logger.info(self.updated_currency)
        return self.updated_currency, self.log_info
