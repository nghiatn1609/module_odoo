# -*- coding: utf-8 -*-
{
    'name': "Purchase Request",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product'],

    # always loaded
    'data': [
        'security/purchase_request_groups.xml',
        'security/ir.model.access.csv',
        'data/purchase_request_data.xml',
        'views/purchase_request_view.xml',
        'views/purchase_request_line_view.xml',
        'views/purchase_request_menu.xml',
        'views/purchase_request_line_menu.xml',
        'security/security.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
