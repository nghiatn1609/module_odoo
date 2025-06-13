# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    is_auto_einvoice_issuance = fields.Boolean(string="Phát hàng hóa đơn điện tử tự động", default=False)
