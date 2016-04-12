# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Payroll Localization - Costa Rica',
    'version': '9.0.1.0',
    'category': 'Localization',
    'sequence': 38,
    'author': 'ClearCorp',
    'website': 'http://www.clearcorp.cr',
    'depends': [
        'hr_payroll_extended',
        'report_xls_template',
    ],
    'data': [
        'data/l10n_cr_hr_payslip_action_data.xml',
        'data/l10n_cr_hr_payroll_salary_rule_category.xml',
        'data/l10n_cr_hr_payroll_salary_rule.xml',
        'data/report_paperformat.xml',
        'data/l10n_cr_hr_payroll_inputs.xml',
        'hr_config_settings.xml',
        'l10n_cr_hr_payroll_view.xml',
        'security/l10n_cr_hr_payroll_security.xml',
        'security/ir.model.access.csv',
        'views/report_payroll_periods.xml',
        'views/report_payroll_xls.xml',
        'views/report_payroll_periods_employee.xml',
        'views/report_payroll_xls_employee.xml',
        'views/report_payslip_run.xml',
        'views/report_payslip_run_xls.xml',
        'views/report_payslip.xml',
        'wizard/payroll_by_periods.xml',
        'wizard/payroll_by_periods_employee.xml',
        'l10n_cr_hr_payroll_report.xml',
        'l10n_cr_hr_payroll_menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
