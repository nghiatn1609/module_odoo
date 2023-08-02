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
    
    price_unit = fields.Float(string='Unit Price', store=True)
    
    @api.depends('product_id.list_price','qty')
    def _total(self):
        for r in self:
            r.total =  r.qty * r.product_id.list_price


    # @api.depends('product_id', 'product_id.seller_ids','request_id')
    # def _compute_price_unit(self):
    #     for line in self:
    #         supplier_info = line.product_id.seller_ids.filtered(lambda r: r.name.id == line.request_id.partner_id.id)
    #         if supplier_info:
    #             line.price_unit = supplier_info[0].price
    #         else:
    #             line.price_unit = 0.0
                
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            seller_info = self.product_id.seller_ids.sorted('date_start', reverse=True)
            print("id: ",self.request_id)
            print("not id: ",self.request_id)
            
            if seller_info:
                self.uom_id = seller_info[0].product_uom
                self.price_unit = seller_info[0].price
                # print("Có")
            else:
                self.uom_id = self.product_id.uom_id
                self.price_unit = 0.0
                # print("không có")
        else:
            self.uom_id = False
            self.price_unit = 0.0
            # print("Càng không có")