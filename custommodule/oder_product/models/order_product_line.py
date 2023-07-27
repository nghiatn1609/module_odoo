# -*- coding: utf-8 -*-

from odoo import models, fields, api


class oder_product_line(models.Model):
    _name = 'purchase.request.line'
    _description = 'Chi tiết yêu cầu mua hàng'

    
    request_id = fields.Many2one(comodel_name="purchase.request", string="Request By")
    product_id = fields.Many2one(comodel_name="product.template", string="Product ID")
    uom_id = fields.Many2one(comodel_name="uom.uom",string="Unit of Measure")
    qty= fields.Float()
    qty_approve = fields.Float()
    total = fields.Float(string="Total", compute="_total")
    
    @api.depends('product_id.list_price','qty')
    def _total(self):
        for r in self:
            r.total =  r.qty * r.product_id.list_price
