# -*- coding: utf-8 -*-

from odoo import models, fields, api


class oder_product(models.Model):
    _name = 'purchase.request'
    _description = 'Yêu cầu mua hàng'


    Department_id = fields.Many2one(comodel_name="hr.department", string="Department")
    Request_id = fields.Many2one('res.users', string="Request By")
    Approver_id = fields.Many2one('res.users', string="Approved By")
    Date = fields.Date(default=fields.Date.today)
    Date_approve = fields.Date(string="Date Approve")
    Request_line_ids = fields.One2many(comodel_name="purchase.request.line", inverse_name='request_id',string='Request by who')
    Description = fields.Text()
    State = fields.Selection([('draft','draft'),
                              ('wait','wait'),
                              ('approve','approve'),
                              ('cancel','cancel')],
                            string="State", help="State of request order", default='draft')
    Total_qty = fields.Float(string="Total Quantity", compute="_get_total_qty")
    Total_Amount = fields.Float(string="Total Amount", compute ="_get_total_amount")
    
    
    @api.depends('Request_line_ids.Qty')
    def _get_total_qty(self):
        for r in self:
           r.Total_qty += r.Request_line_ids.Qty
                
    
    @api.depends('Request_line_ids.Total')
    def _get_total_amount(self):
        for r in self:
            r.Total_Amount += r.Request_line_ids.Total 