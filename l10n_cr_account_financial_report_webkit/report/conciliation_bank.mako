<html>
    <head>
        <style type="text/css">
            ${css}

            .list_table .act_as_row {
                margin-top: 10px;
                margin-bottom: 10px;
                font-size:10px;
            }

            .account_line {
                font-weight: bold;
                font-size: 15px;
                background-color:#F0F0F0;
            }
            
            .account_line .act_as_cell {
                height: 30px;
                vertical-align: bottom;
            }

        </style>
    </head>
<body class = "data">
    %for account in objects :
        <%
        bank_accounts = get_bank_accounts(cr, uid, account.id, context)
        bank_balance = get_bank_balance(cr, uid, bank_accounts, context)
        %>
        <%setLang(user.context_lang)%>

        <div style="font-size: 20px; font-weight: bold; text-align: center;"> ${company.partner_id.name | entity} - ${company.currency_id.name | entity}</div>
        <div style="font-size: 25px; font-weight: bold; text-align: center;"> Conciliación de Bancos</div>
        <div style="font-size: 20px; font-weight: bold; text-align: center;"> ${account.name}</div>
        </br></br>
        
        <div class="act_as_table data_table" style="margin-top:30px">
        <div class="act_as_row labels">
            <div class="act_as_cell" style = "text-align: left;">${_('Bank Balance')}</br>
            ${_('Conciled Balance')}</br>
            ${_('Cobros')}</br>
            ${_('Payments')}</br>
            ${_('Debits')}</br>
            ${_('Credits')}</br>
            ${_('Total')}</br>
            </div>
            <div class="act_as_cell" style = "text-align: left;">${formatLang(bank_balance[0])}</br>
            ${formatLang(bank_balance[0])}</br>
            ${formatLang(bank_balance[1])}</br>
            ${formatLang(bank_balance[2])}</br>
            ${formatLang(bank_balance[3])}</br>
            ${formatLang(bank_balance[4])}</br>
            <% total = bank_balance[0] + bank_balance[1] + bank_balance[2] + bank_balance[3] + bank_balance[4]%>
            ${formatLang(total)}
            </div>
        </div>
        </div>
        
        <div class="account_title bg" style="width: 100%; margin-top: 15px; font-size: 12px;">${_('Move Lines')}</div>
        <div class="act_as_table list_table" style="margin-top: 5px;">
        <div class="act_as_thead">
            <div class="act_as_row labels">
                ## Account
                <div class="act_as_cell first_column" style="width: 150px;">${_('Account')}</div>
                ## Partner
                <div class="act_as_cell" style="width: 150px;">${_('Partner')}</div>
                ## date
                <div class="act_as_cell" style="width: 70px;">${_('Date')}</div>
                ## period
                <div class="act_as_cell" style="width: 70px;">${_('Period')}</div>
                ## journal
                <div class="act_as_cell" style="width: 70px;">${_('Journal')}</div>
                ## label
                <div class="act_as_cell" style="width: 270px;">${_('Label')}</div>
                 ## Invoices
                <div class="act_as_cell amount" style="width: 100px;">${_('Invoice')}</div>
                ## credit
                <div class="act_as_cell amount" style="width: 100px;">${_('Payments')}</div>
                ## debit
                <div class="act_as_cell amount" style="width: 100px;">${_('Credit')}</div>
                ## Payments
                <div class="act_as_cell amount" style="width: 100px;">${_('Debit')}</div>
                ## balance cumulated
                <div class="act_as_cell amount" style="width: 115px;">${_('Cumul. Bal.')}</div>
            </div>
        </div>
        <div class="act_as_tbody">
            <%
            total_invoice = 0.0
            total_payment = 0.0
            total_debit = 0.0
            total_credit = 0.0
            accumulated_balance = 0.0
            accumulated_balance_curr = 0.0
            total_accumulated_balance = 0.0
            %>
            %for bank_account in bank_accounts:
                <%move_lines = [] %>
                %if bank_account.user_type.name != 'Banco Saldo Real':
                    <% move_lines = get_move_lines(cr, uid, bank_account.id, context=None) %>
                      
                    %for line in move_lines:
                      <%
                          invoice_amount = 0.0
                          payment_amount = 0.0
                          credit_amount = 0.0
                          debit_amount = 0.0
        
                          amount = get_amount(cr, uid, line, bank_account.currency_id.id)
                      %>
                      <div class="act_as_row lines">
                          ## Account
                          <div class="act_as_cell first_column">${line.account_id.name}</div>
                          ## Partner
                          <div class="act_as_cell">${line.partner_id.name}</div>
                          ## date
                          <div class="act_as_cell">${formatLang(line.date, date=True)}</div>
                          ## period
                          <div class="act_as_cell">${line.period_id.name}</div>
                          ## journal
                          <div class="act_as_cell">${line.journal_id.name}</div>
                          ## label
                          <div class="act_as_cell">${line.name}</div>
                          ## Invoice
                          <div class="act_as_cell amount">
                          %if amount[0] == 'invoice':
                            <%
                            invoice_amount = amount[1]
                            total_invoice += invoice_amount
                            %>
                            ${ formatLang(invoice_amount or 0.0) }
                          %else:
                            ${'0.0'}
                          %endif
                          %if amount[2] != None and amount[0] == 'invoice':
                            ${' ('}${ formatLang(amount[2]) }${')'}
                          %endif
                          </div>
                          ## Payment
                          <div class="act_as_cell amount">
                          %if amount[0] == 'payment':
                            <%
                            payment_amount = amount[1]
                            total_payment += payment_amount
                            %>
                            ${ formatLang(payment_amount or 0.0) }
                          %else:
                            ${'0.0'}
                          %endif
                          %if amount[2] != None and amount[0] == 'payment':
                            ${' ('}${ formatLang(amount[2]) }${')'}
                          %endif
                          </div>
                          ## Credit
                          <div class="act_as_cell amount">
                          %if amount[0] == 'credit':
                            <%
                            credit_amount = amount[1]
                            total_credit += credit_amount
                            %>
                            ${ formatLang(credit_amount or 0.0) }
                          %else:
                            ${'0.0'}
                          %endif
                          %if amount[2] != None and amount[0] == 'credit':
                            ${' ('}${ formatLang(amount[2]) }${')'}
                          %endif
                          </div>
                          ## Debit
                          <div class="act_as_cell amount">
                          %if amount[0] == 'debit':
                            <%
                            debit_amount = amount[1]
                            total_debit += debit_amount
                            %>
                            ${ formatLang(debit_amount or 0.0) }
                          %else:
                            ${'0.0'}
                          %endif
                          %if amount[2] != None and amount[0] == 'debit':
                            ${' ('}${ formatLang(amount[2]) }${')'}
                          %endif
                          </div>
                          ## balance cumulated
                          <% 
                            accumulated_balance = (invoice_amount+payment_amount+credit_amount+debit_amount) or 0.0
                            total_accumulated_balance += accumulated_balance 
                          %>
                          <div class="act_as_cell amount" style="padding-right: 1px;">${formatLang(total_accumulated_balance) }</div>
                    </div>
                    %endfor
                %endif
                %endfor
                <div class="act_as_table list_table" style="margin-top:5px;">
                        <div class="act_as_row labels" style="font-weight: bold; font-size: 12px;">
                            ## label
                            <div class="act_as_cell" style="width: 150px;">${_("Total")}</div>
                            <div class="act_as_cell" style="width: 150px;">${_('')}</div>
                            <div class="act_as_cell" style="width: 70px;">${_('')}</div>
                            <div class="act_as_cell" style="width: 70px;">${_('')}</div>
                            <div class="act_as_cell" style="width: 70px;">${_('')}</div>
                            <div class="act_as_cell" style="width: 270px;">${_('')}</div>
                            %if account.currency_id.id != False:
                                ## invoice
                                <div class="act_as_cell amount" style="width: 100px;">${formatLang(total_invoice)}</div>
                                ## payment
                                <div class="act_as_cell amount" style="width: 100px;">${formatLang(total_payment)}</div>
                                ## credit
                                <div class="act_as_cell amount" style="width: 100px;">${formatLang(total_credit)}</div>
                                ## debit
                                <div class="act_as_cell amount" style="width: 100px;">${formatLang(total_debit)}</div>
                                ## balance cumulated
                                <div class="act_as_cell amount" style="width: 115px;">${formatLang(total_accumulated_balance)}</div>
                            %else:
                                ## invoice
                                <div class="act_as_cell amount" style="width: 100px;">${company.currency_id.symbol} ${formatLang(total_invoice)}</div>
                                ## payment
                                <div class="act_as_cell amount" style="width: 100px;">${company.currency_id.symbol} ${formatLang(total_payment)}</div>
                                ## credit
                                <div class="act_as_cell amount" style="width: 100px;">${company.currency_id.symbol} ${formatLang(total_credit)}</div>
                                ## debit
                                <div class="act_as_cell amount" style="width: 100px;">${company.currency_id.symbol} ${formatLang(total_debit)}</div>
                                ## balance cumulated
                                <div class="act_as_cell amount" style="width: 115px;">${company.currency_id.symbol} ${formatLang(total_accumulated_balance)}</div>
                            %endif
                        </div>
                    </div>
            </div>
        </div>
    %endfor

</body>
</html>
