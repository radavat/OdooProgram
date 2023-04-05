# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Restaurant Project',
    'version' : '1.0.1.1',
    'summary': 'Restaurant Project will help in the management of Restaurant.',
    'sequence': -100,
    'description': """Restaurant Project will help in the management of Restaurant, which give us all data of our restaurent like orders, staff,customers and items""",
    'category': 'Sale and Invoicing',
    'website': 'https://www.odoo.com/',
    'images' : [],
    'depends' : ['base','mail','sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/department_view.xml',
        'wizard/staff_view_wizard.xml',
        'views/staff_view.xml',
        'views/menu_view.xml',
        'reports/staff_report.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
