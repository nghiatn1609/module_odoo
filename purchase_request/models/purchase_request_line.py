# -*- coding: utf-8 -*-

from odoo import models, fields, api


class purchase_request_line(models.Model):
    _name = 'purchase.request.line'
    _description = 'Chi tiết yêu cầu mua hàng'

    
    request_id = fields.Many2one(comodel_name="purchase.request",string="Request By", required=True)
    product_id = fields.Many2one(comodel_name="product.template", string="Product ID", required=True)
    uom_id = fields.Many2one(comodel_name="uom.uom",string="Unit of Measure", required=True)
    qty= fields.Float()
    qty_approve = fields.Float()
    total = fields.Float(string="Total", compute="_total")
    
    # price_unit = fields.Float(string='Unit Price', compute='_compute_price_unit', store=True)
    
    @api.depends('product_id.list_price','qty')
    def _total(self):
        for r in self:
            r.total =  r.qty * r.product_id.list_price


    # @api.depends('product_id', 'product_id.seller_ids')
    # def _compute_price_unit(self):
    #     for line in self:
    #         supplier_info = line.product_id.seller_ids.filtered(lambda r: r.name.id == line.request_id.partner_id.id)
    #         if supplier_info:
    #             line.price_unit = supplier_info[0].price
    #         else:
    #             line.price_unit = 0.0