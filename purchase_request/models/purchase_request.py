# -*- coding: utf-8 -*-

from odoo import models, fields, api
import xlsxwriter
from odoo import exceptions

class purchase_request(models.Model):
    _name = 'purchase.request'
    _description = 'Yêu cầu mua hàng'


    name = fields.Char(string='Name', readonly=True, required=True, copy=False, default='New')


    request_id = fields.Many2one('res.users', string="Request By", required=True, default=lambda self: self.env.user)
    department_id = fields.Many2one(comodel_name="hr.department", string="Department", required=True,
                                    default= lambda self: self.env.user.department_id) 
                                                    #  self.env.user.department_id.id
    approver_id = fields.Char(string="Approved By", required=True, 
                              related='department_id.manager_id.name', readonly=False)
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
    reason_rejection = fields.Text(string='Reason for Rejection')

     # Add a boolean field to track if the record is in 'Edit' state
    is_editing = fields.Boolean(string='Is Editing', compute='_compute_is_editing')

    

    def action_send_request(self):
        print("Gửi yêu cầu")
    
    def action_approve(self):
        group_manager = self.env.ref('purchase_request.group_purchase_request_manager')
        if group_manager in self.env.user.groups_id:
            self.state = 'approve'
        else:
            raise exceptions.UserError("You do not have permission to approve this request.")

    def action_reject(self):
        group_manager = self.env.ref('purchase_request.group_purchase_request_manager')
        if group_manager in self.env.user.groups_id:
            view_id = self.env.ref('purchase_request.view_reject_reason_form').id
            # self.state = 'cancel'
            return {
                'name': 'Reason for Rejection',
                'view_mode': 'form',
                'view_id': view_id,
                'res_model': 'purchase.request',
                'res_id': self.id,
                'type': 'ir.actions.act_window',
                'target': 'new',
            }
        else:
            raise exceptions.UserError("You do not have permission to reject this request.")


    def action_confirm_reject(self):
        self.write({'state': 'cancel', 'reason_rejection': self.reason_rejection})
        
    def action_return(self):
        print("Return")

    
    
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
        return super(purchase_request, self).create(vals)
    
    
    @api.depends('state')
    def _compute_is_editing(self):
        for record in self:
            record.is_editing = record.state == 'draft'