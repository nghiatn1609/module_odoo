# -*- coding: utf-8 -*-

from odoo import models, fields, api
import xlsxwriter


class oder_product(models.Model):
    _name = 'purchase.request'
    _description = 'Yêu cầu mua hàng'


    name = fields.Char(string='Name', readonly=True, required=True, copy=False, default='New')


    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=True)
    request_id = fields.Many2one('res.users', string="Request By", required=True)
    approver_id = fields.Many2one('res.users', string="Approved By", required=True)
    date = fields.Date(default=fields.Date.today)
    date_approve = fields.Date(string="Date Approve")
    request_line_ids = fields.One2many(comodel_name="purchase.request.line", inverse_name='request_id',string='Request by who')
    description = fields.Text()
    state = fields.Selection([('draft','draft'),
                              ('wait','wait'),
                              ('approve','approve'),
                              ('cancel','cancel')],
                            string="State", help="State of request order", default='draft')
    total_qty = fields.Float(string="Total Quantity", compute="_get_total_qty", store=True)
    total_amount = fields.Float(string="Total Amount", compute ="_get_total_amount", store=True)
    
    def action_send_request(self):
        print("Gửi yêu cầu")
    
    def export_to_excel(self):
        # Create a new Excel workbook and add a worksheet
        workbook = xlsxwriter.Workbook('purchase_requests_1.xlsx')
        worksheet = workbook.add_worksheet()

        # Write the headers
        headers = ['Request ID', 'Product ID', 'Quantity', 'Total Price']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)

        # Write the data rows
        row = 1
        for request in self.filtered(lambda r: r.state == 'approve'):
            for line in request.request_line_ids:
                worksheet.write(row, 0, request.name)
                worksheet.write(row, 1, line.product_id.name)
                worksheet.write(row, 2, line.qty)
                worksheet.write(row, 3, line.total)
                row += 1

        # Close the workbook
        workbook.close()
    
    
    @api.depends('request_line_ids.qty')
    def _get_total_qty(self):
        for r in self:
            r.total_qty = sum(st.qty for st in r.request_line_ids)
                
    
    @api.depends('request_line_ids.total')
    def _get_total_amount(self):
        for r in self:
            r.total_amount = sum(st.total for st in r.request_line_ids)
            
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request') or '/'
        return super(oder_product, self).create(vals)
    
    
    