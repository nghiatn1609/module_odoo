# -*- coding: utf-8 -*-
{
    'name': "Account SInvoice",

    'summary': """""",

    'description': """""",

    'author': "ERPVIET",
    'website': "https://erpviet.vn",
    'category': 'Accounting',
    'version': '13.0.1.0.0',
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'depends': ['point_of_sale', 'base', 'ev_pos_session_queue', 'ev_pos_refund', 'product', 'ev_pos_receipt'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/ir_config_parameter.xml',
        'data/ir_cron.xml',
        'views/pos_order_views.xml',
        'views/res_company_views.xml',
        'views/create_sinvoice_lot_views.xml',
        'views/pos_config_views.xml',
        'views/account_sinvoice_views.xml',
        'views/pos_order_line_views.xml',
        'views/product_template_views.xml',
        'views/pos_payment_method_views.xml',
        'views/assets.xml',
        'wizard/wizard_confirm_view.xml'
    ],
    'qweb': [
        'static/src/xml/PaymentScreen.xml',
        'static/src/xml/receipt.xml',
    ],
}
