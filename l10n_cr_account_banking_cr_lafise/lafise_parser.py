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
"""
Parser for Lafise html format files
"""
import re
from datetime import datetime
from dateutil import parser
from pprint import PrettyPrinter
from copy import copy
from tools.translate import _
from osv import osv, fields

class LafiseParser(object):
    
    #Define the header for the extract to import.
    '''
     ** Kwargs parameter is used for a dynamic list of parameters. 
        The wizard imported extracts used in all parsers and not all parsers have all the necessary information in your file, 
        so get information from the wizard and passed by the ** kwargs. 
        Then in the parses that are needed, are extracted from the ** kwargs and if needed, 
        the parser still works the same way without this parameter.
        
        The rest of the methods must receive this parameter. (As the method that parse the header and the lines). 
        
        If you need a new parameter, you specify its name and value, using the ** kwargs is a dictionary, 
        extract its value, with the respective key
    '''
    
    """
        As the lafise file comes in a html format, the parameter rows is the file parser, 
        the values can be extracted with the property .text in the row.
        For the header, extracted the account, currency, initial_balance, ending_balance. 
        
        It must iterate in the rows to obtain the values.
    """    
    
    def statement_record ( self, rows, **kwargs):
        lines = []
        line_dict = {}
        count = 1
        currency_code = ''
        
        line_dict = {
            'transref': '', # _transmission_number
            'account_number': '', #_account_number
            'statementnr':'', # statement_number
            'startingbalance': 0.0, #_opening_balance
            'currencycode': '', #currencycode
            'endingbalance': 0.0, #_closing_balance
            'bookingdate': '', #moving_date
            'ammount': 0.0,
            'id': '',
        }        
        #transmission_number and bookingdate -> Date when make the extract import.
        date_obj= datetime.now()
        line_dict['transref'] = date_obj
        
        #delete blank rows
        for row in rows:
            values = [col.text for col in row]
            if len(values) > 0:
                lines.append(values)
        
        #lines is a list of lists.        
        #First, check if the account in the wizard match with the account in the file. 
        if self.match_account(lines, kwargs['account_number']):        
            #extract from the wizard the account
            line_dict['account_number'] = kwargs['account_number']           
            
            for list in lines:
                #currency_code in th file
                if count == 4:
                    currency = list[4]
                    
                    if "COL" in currency:
                        currency_code = 'CRC'
                        
                    elif "USD" in currency:
                        currency_code = 'USD'
                    
                    line_dict['currencycode'] = currency_code
                
                #initial balance
                if count == 16:
                    line_dict['startingbalance'] =  self.extract_float(str(list[5]).replace(",",""))
                
                #interrupted the cycle, because the information is complete for the header.
                elif count >= 24:
                    break               
                count +=1        
            
            #statementnr
            line_dict['statementnr'] = kwargs['date_from_str'] + ' - '+ kwargs['date_to_str'] + ' Extracto Lafise ' + line_dict['account_number'] #Interval time of the file.
                                    
            #bookingdate
            line_dict['bookingdate'] = date_obj
            
            #id
            line_dict['id'] = kwargs['date_from_str'] + ' - '+ kwargs['date_to_str'] + ' Extracto Lafise ' + line_dict['account_number']            
             
            #ending_balance 
            list = self.clean_special_characters_list(lines) #clean all the special characters and the rows without information
            result = self.calculate_final_balance(list)
            line_dict['endingbalance'] = float(line_dict['startingbalance']) - float(result['debit']) + float(result['credit'])
            
            #amount
            line_dict['ammount'] = float(line_dict['startingbalance']) + float(line_dict['endingbalance'])
            
            return line_dict
        
        else:
             raise osv.except_osv(_('Error'),
                        _('Error en la importación! La cuenta especificada en el archivo no coincide con la seleccionada en el asistente de importacion'))
             
    '''
    Parse all the lines in the file. Once the header is parser, the next step are the lines.
    '''     
    def statement_lines (self, records, rows):
        parser = LafiseParser()
        line_id = 1 #To distinct the lines, in the case of someone are repeat. 
        
        mapping = {
            'execution_date' : '',
            'effective_date' : '',
            'transfer_type' : '',
            'reference' : '',
            'message' : '',
            'name' : '',
            'transferred_amount': '',
            'creditmarker': '',
        }
        
        lines = clean_list = []
        statements = [] 
        currencycode = records['currencycode']
        count = 1 #in line 18 start the statements.
        
        #delete blank rows
        for row in rows:
            values = [col.text for col in row]
            if len(values) > 0:
                lines.append(values)
        
        #clear lines of special characters
        clean_list = self.clean_special_characters_list(lines)

        for line in clean_list:
            #effective_date                  
            date_str = self.extract_date_regular_expresion(self.clean_special_characters(line[0]))
            date = datetime.strptime(date_str, "%d/%m/%y")               
            mapping['effective_date'] = date #fecha_contable.
            
            #execution_date
            mapping['execution_date'] = date #fecha_movimiento                       
           
            str_line = self.clean_special_characters(line[2]) + ' ID line: ' + str(line_id)
            
            mapping['local_currency'] = currencycode
            mapping['transfer_type'] = 'NTRF'
            mapping['reference'] = self.extract_number(self.clean_special_characters(line[1]))
            mapping['message'] = str_line               
            mapping['name'] = str_line
            mapping['id'] = str_line
            
            debit = float(self.extract_float(self.clean_special_characters(line[3])))
            credit = float(self.extract_float(self.clean_special_characters(line[4])))
                            
            if (credit > 0.0): #in this case, credit is a input of money
                mapping['transferred_amount'] = credit
                mapping['creditmarker'] = 'C'
                                  
            else: #debit is output
                mapping['transferred_amount'] =  -debit
            
            statements.append(copy(mapping))
            line_id += 1

        return statements    
    
    """
    ** Kwargs parameter is used for a dynamic list of parameters. 
        The wizard imported extracts used in all parsers and not all parsers have all the necessary information in your file, 
        so get information from the wizard and passed by the ** kwargs. 
        Then in the parses that are needed, are extracted from the ** kwargs and if needed, 
        the parser still works the same way without this parameter.
        
        The rest of the methods must receive this parameter. (As the method that parse the header and the lines). 
        
        If you need a new parameter, you specify its name and value, using the ** kwargs is a dictionary, 
        extract its value, with the respective key
    """
    def parse_stamenent_record( self, rec, **kwargs):

        matchdict = dict()
        
        #Set the header for the stament.
        matchdict = self.statement_record(rec, **kwargs);
        
        return matchdict
        
    def parse( self, cr, data ):
        records = []
        # Some records are multiline
        for line in data:
            if len(line) <= 1:
                continue
            if line[0] == ':' and len(line) > 1:
                records.append(line)
            else:
                records[-1] = '\n'.join([records[-1], line])
                
        output = []

        for rec in records:
            output.append( self.parse_stamenent_record( rec ) )
                
        return output
    
    ##################################<-AUXILIAR METHODS->####################################
    def extract_number( self, account_number ):
        cad = ''
        result = re.findall(r'[0-9]+', account_number)
               
        for character in result:
            cad = cad + character
        return cad

    def extract_float ( self, ammount ):
        cad = ''
        result = re.findall(r"[-+]?\d*\.\d+|\d+",ammount)
        
        for character in result:
            cad = cad + character       
        return cad
    
    def extract_date_regular_expresion(self, date):
        cad = ''
        result = []
        date_string = ''
        result = re.findall('[0-9]{1,2}/[0-9]{1,2}/[0-9]{2}', date)
       
        for character in result:
            cad = cad + character       
        return cad
    
    #clear special characters in a specific celd. 
    def clean_special_characters(self, text_celd):
        special_characters = {'\r\n':'','\t':''}
        
        for i, j in special_characters.iteritems():
            text = text_celd.replace(i, j)    
        
        #remove all the blank space.
        #return re.sub(r'\s', '', text)
        return text
    
    #clear special characters in a specific row. 
    def clean_special_characters_list(self, lines):    
        new_row = list = []
        special_characters = {'\r\n':'','\t':'','\r':'','\n':'','\\t':'','\t':''}
        count = 1

        for l in lines:
            if (count >= 18): #in the line 18 start the statements                
                if len(list) == 0:
                    list = []
                    
                for celd in l:
                    if celd != None:
                        for i, j in special_characters.iteritems():
                            text = celd.replace(i, j)
                            text = re.sub(r'\t', '', text) #'\t' is the "tab" character
                            
                        if text != '':                      
                            new_row.append(text)
                
                if len(new_row) > 0:
                    list.append(new_row) #list containt all the rows clean 
                new_row = []

            count +=1
            
        return list
    
    #Return true if the account selected in the wizard match with the account in the file.
    def match_account(self, lines, account_wizard):
        count = 1
        acc_number = ''
        for list in lines:
            if count == 4:
                acc_number= self.extract_number(list[1])
                break
            else:
                count +=1
        
        if acc_number.find(account_wizard) > -1:
            return True
        
        else:
            return False
    
    #List is the list of the statements, the method calculate the final_balance 
    #with the debit and credit
    def calculate_final_balance(self, list):
        result = {'debit': 0.0, 'credit':0.0}
        total_debit = total_credit = 0.0
        
        for line in list:
            debit = float(self.extract_float(self.clean_special_characters(line[3])))
            credit = float(self.extract_float(self.clean_special_characters(line[4])))
            
            total_debit += debit
            total_credit += credit
        
        result ['debit'] = total_debit
        result ['credit'] = total_credit
        
        return result
        