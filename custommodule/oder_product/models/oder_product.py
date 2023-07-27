# -*- coding: utf-8 -*-

from odoo import models, fields, api


class oder_product(models.Model):
    _name = 'purchase.request'
    _description = 'Yêu cầu mua hàng'


    department_id = fields.Many2one(comodel_name="hr.department", string="Department")
    request_id = fields.Many2one('res.users', string="Request By")
    approver_id = fields.Many2one('res.users', string="Approved By")
    date = fields.Date(default=fields.Date.today)
    date_approve = fields.Date(string="Date Approve")
    request_line_ids = fields.One2many(comodel_name="purchase.request.line", inverse_name='request_id',string='Request by who')
    description = fields.Text()
    state = fields.Selection([('draft','draft'),
                              ('wait','wait'),
                              ('approve','approve'),
                              ('cancel','cancel')],
                            string="State", help="State of request order", default='draft')
    total_qty = fields.Float(string="Total Quantity", compute="_get_total_qty")
    total_Amount = fields.Float(string="Total Amount", compute ="_get_total_amount")
    
    
    @api.depends('request_line_ids.qty')
    def _get_total_qty(self):
        for r in self:
           r.total_qty += r.request_line_ids.qty
                
    
    @api.depends('request_line_ids.total')
    def _get_total_amount(self):
        for r in self:
            r.total_Amount += r.request_line_ids.total 
