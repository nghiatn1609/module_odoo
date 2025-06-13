# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    release_sinvoice_name = fields.Char(
        string='Tên xuất HDDT', required=True,
        help="Tên phát hành SInvoice sẽ được sử dụng để xác định hóa đơn điện tử.",
    )

    def action_update_tax(self):
        products = self.search([('type', '=', 'product')])
        tax_id = self.env['account.tax'].search([('amount', '=', 8)], limit=1)
        for product in products:
            product.taxes_id = tax_id