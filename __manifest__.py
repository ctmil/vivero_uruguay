# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Vivero Uruguay',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Plants and customers management',
    'depends': ['web','product'],
    'data': [
        'security/ir.model.access.csv',
        #'data/data.xml',
        'uruguay_view.xml',
        ],
    'demo': [
        ],
    'css': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
