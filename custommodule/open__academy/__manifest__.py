# -*- coding: utf-8 -*-
{
    'name': "Open_Academy",
    'sequence' : -100,
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
    'depends': ['base'],

    # always loaded
    'data': [
        'views/views_course.xml',
        'views/views_session.xml',
        'views/menu.xml',
        'views/partner.xml',
        'views/templates.xml',
        'reports/course_report.xml',
        'reports/course_templates.xml',
        'demo/demo.xml',
        'security/model_groups.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
