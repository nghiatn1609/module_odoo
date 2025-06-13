# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import requests
from datetime import datetime, timedelta
import json
import logging
import math


class PosOrder(models.Model):
    _inherit = 'pos.order'

    sinvoice_id = fields.Many2one('account.sinvoice', string='Account SInvoice', copy=False)
    sinvoice_lot_id = fields.Many2one('create.sinvoice.lot', string='Create SInvoice Lot', copy=False)
    sinvoice_no = fields.Char(string='SInvoice No', size=15, copy=False,
                              help='Invoice No (eg: K23TAA00000001, K23TAA: invoice symbol, 00000001: incre number)')
    sinvoice_series = fields.Char(string='SInvoice Series', size=20, help='Invoice symbol, eg: K23TAA', copy=False)
    sinvoice_issued_date = fields.Datetime(string='SInvoice Issued Date', help='Invoice issued date', copy=False)
    sinvoice_state = fields.Selection([
        ('no_release', 'No Release'),
        ('released', 'Released'),
        ('queue', 'Queue'),
        ('cancel_release', 'Cancel Release')
    ], string='SInvoice State', copy=False)

    sinvoice_vat = fields.Char(string='SInvoice VAT', size=20, copy=False)
    sinvoice_company_name = fields.Char(string='SInvoice Company Name', size=1200, copy=False)
    sinvoice_address = fields.Char(string='SInvoice Address', size=1200, copy=False)
    sinvoice_email = fields.Char(string='SInvoice Email', size=1200, copy=False)
    transaction_uuid = fields.Char(string='Transaction Uuid', copy=False, index=True)
    sinvoice_customer_type = fields.Selection([
        ('personal', 'Cá nhân'),
        ('company', 'Công ty')
    ], string='Loại khách hàng', default='personal', copy=False, help='Loại khách hàng của hóa đơn điện tử, cá nhân hoặc công ty')
    sinvoice_buyer_get_invoice = fields.Boolean(string='Khách hàng lấy hóa đơn', default=False, copy=False)
    sinvoice_customer_name = fields.Char(string='Tên khách hàng', size=1200, copy=False)
    sinvoice_customer_id = fields.Char(string='CCCD/MSTCN', size=20, copy=False, help='Mã khách hàng của hóa đơn điện tử')

    def get_partner_info_sinvoice(self, partner_id):
        sql = """
            SELECT sinvoice_vat,
                   sinvoice_company_name,
                   sinvoice_address,
                   sinvoice_email
            FROM pos_order po
            WHERE po.partner_id = %s
            AND po.sinvoice_vat IS NOT NULL
            AND po.sinvoice_vat != ''
            ORDER BY po.id DESC
            LIMIT 1;
        """
        self._cr.execute(sql % int(partner_id))
        res = self._cr.dictfetchall()
        if len(res) > 0:
            return res[0]
        return None

    @api.model
    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        
        # Các trường hiện tại
        res['sinvoice_vat'] = str(ui_order.get('x_sinvoice_vat') or '')
        res['sinvoice_company_name'] = str(ui_order.get('x_sinvoice_company_name') or '')
        res['sinvoice_address'] = str(ui_order.get('x_sinvoice_address') or ui_order.get('x_sinvoice_customer_address') or '')
        res['sinvoice_email'] = str(ui_order.get('x_sinvoice_email') or ui_order.get('x_sinvoice_customer_email') or '')
        
        # Thêm các trường mới theo yêu cầu
        res['sinvoice_buyer_get_invoice'] = bool(ui_order.get('x_sinvoice_buyer_get_invoice'))
        res['sinvoice_customer_type'] = str(ui_order.get('x_sinvoice_customer_type') or '')
        res['sinvoice_customer_name'] = str(ui_order.get('x_sinvoice_customer_name') or '')
        res['sinvoice_customer_id'] = str(ui_order.get('x_sinvoice_customer_id') or '')
        
        return res

    # @api.model
    # def write(self, vals):
    #     res = super(PosOrder, self).write(vals)
    #     if 'state' in vals and vals[
    #         'state'] == 'paid' and self.x_allow_return == True and self.x_pos_order_refund_id != None:
    #         order_original = self.env['pos.order'].search([('id', '=', self.x_pos_order_refund_id.id)])
    #         if order_original and order_original.sinvoice_state == 'released':
    #             val = {
    #                 'action_type': 'cancel',
    #                 'line_ids': self
    #             }
    #             create_sinvoice_lot = self.env['create.sinvoice.lot'].create(val)
    #             create_sinvoice_lot.action_api_destroy_sinvoice(self)
    #     return res

    def action_api_destroy_sinvoice(self):
        try:
            order_origin = self.x_pos_order_refund_id
            time_now = datetime.now()
            company = self.env.company
            sinvoice_type = company.sinvoice_type
            sinvoice_template_code = company.sinvoice_template_code
            sinvoice_series = company.sinvoice_series
            url = company.sinvoice_production_url + '/InvoiceAPI/InvoiceWS/cancelTransactionInvoice'
            payload = {
                'supplierTaxCode': str(company.vat),
                'templateCode': sinvoice_template_code,
                'invoiceNo': order_origin.sinvoice_no,
                'strIssueDate': int(order_origin.sinvoice_issued_date.timestamp()) * 1000,
                'additionalReferenceDesc': self.name,
                'additionalReferenceDate': int(self.date_order.timestamp()) * 1000,
                'reasonDelete': self.x_note_return or '',
            }
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            auth = requests.auth.HTTPBasicAuth(username=company.sinvoice_username, password=company.sinvoice_password)
            response = requests.request('POST', url, headers=headers, data=payload, auth=auth)
            res = json.loads(response.text)
            if 'errorCode' in res and not res['errorCode']:
                order_origin.sinvoice_state = 'cancel_release'
                order_origin.sinvoice_id.sinvoice_state = 'cancel_release'
                order_origin.sinvoice_id.sinvoice_cancel_date = self.date_order
                self._cr.commit()
            else:
                result = {
                    'params': payload,
                    'response': response.text
                }
                raise ValidationError(str(result))
        except Exception as ex:
            raise ValidationError(ex)
        
    def action_api_adjust_sinvoice(self):
        try:
            company = self.env.company
            url = company.sinvoice_production_url + '/InvoiceAPI/InvoiceWS/createInvoice/' +  company.vat
            payload = self._prepare_adjust_data(company)
            headers = {
                'Content-Type': 'application/json'
            }
            auth = requests.auth.HTTPBasicAuth(username=company.sinvoice_username, password=company.sinvoice_password)
            response = requests.request('POST', url, headers=headers,data=json.dumps(payload), auth=auth)
            res = json.loads(response.text)
            if 'errorCode' in res and not res['errorCode']:
                self._cr.commit()
            else:
                result = {
                    'params': payload,
                    'response': response.text
                }
                raise ValidationError(str(result))
        except Exception as ex:
            raise ValidationError(ex)

    def action_update_invoice_no(self):
        time_now = datetime.now() + timedelta(hours=7) - timedelta(days=1)
        time_compare = datetime(time_now.year, time_now.month, time_now.day).strftime('%Y-%m-%d')
        
        sql = """
            SELECT id FROM pos_order
            WHERE (date_order + INTERVAL '7 hours')::date = '%s'
             AND sinvoice_state = 'released'
             AND sinvoice_no IS NULL OR sinvoice_no  = ''
        """
        self._cr.execute(sql % (time_compare))
        orders = self._cr.dictfetchall()

        company = self.env.company
        url = company.sinvoice_production_url + '/InvoiceAPI/InvoiceWS/searchInvoiceByTransactionUuid'
        auth = requests.auth.HTTPBasicAuth(username=company.sinvoice_username,
                                           password=company.sinvoice_password)
        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        for item in orders:
            order = self.env['pos.order'].search([('id', '=', item['id'])])
            if order.sinvoice_state == 'released':
                payload = {
                    'supplierTaxCode': str(company.vat),
                    'transactionUuid': order.pos_reference
                }
                response = requests.request('POST', url, headers=header, data=payload, auth=auth)
                if response.status_code != 200:
                    continue
                res = json.loads(response.text)
                if 'result' in res:
                    order.sinvoice_no = res['result'][0]['invoiceNo']
                    order.sinvoice_issued_date = datetime.fromtimestamp(
                        int(res['result'][0]['issueDate']) // 1000)
                    order.sinvoice_state = 'released'
                    # update account_sinvoice
                    order.sinvoice_id.sinvoice_no = order.sinvoice_no
                    order.sinvoice_id.sinvoice_state = 'released'
                    order.sinvoice_id.sinvoice_date = order.sinvoice_issued_date
                    order.sinvoice_id.order_id = order.id
                    order.sinvoice_id.reservation_code = res['result'][0]['reservationCode']

    def action_export_sinvoice(self):
        self.ensure_one()
        return {
            'name': _('Phát hành HDDT'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.confirm.export.einvoice',
            'target': 'new',
            'view_id': self.env.ref('ev_account_sinvoice.wizard_confirm_form_view').id or False,
            'context': {
                'active_ids': self._context.get('active_ids'),
                'active_model': self._name,
            }
        }
    
    def _prepare_refund_values(self, current_session):
            self.ensure_one()
            return {
                'name': self.name + _(' REFUND'),
                'session_id': current_session.id,
                'date_order': fields.Datetime.now(),
                'pos_reference': 'RF' + (self.pos_reference or ''),
                'lines': False,
                'amount_tax': -self.amount_tax,
                'amount_total': -self.amount_total,
                'amount_paid': 0,
                'x_pos_order_refund_id': self.id,
                'user_id': self.env.uid,
                # 'employee_id': self.env.user.employee_id.id
                'employee_id': self.employee_id.id,  # keep original employee
            }

    def refund(self):
        """Create a copy of order  for refund order"""
        check_refund_order = self.env['pos.order'].search([('x_pos_order_refund_id', '=', self.id)])
        if not check_refund_order:
            if not self.x_note_return:
                raise UserError(_('No reason entered'))
            refund_orders = self.env['pos.order']
            for order in self:
                order._check_data_allow_refund()
                # When a refund is performed, we are creating it in a session having the same config as the original
                # order. It can be the same session, or if it has been closed the new one that has been opened.
                current_session = self.env['pos.session'].sudo().search([
                    ('state', '=', 'opened'),
                    ('user_id', '=', self.env.uid),
                ])
                if not current_session or current_session.state in ('queued'):
                    raise UserError(_('Bạn phải mở một phiên trên POS'))
                refund_order = order.copy(
                    order._prepare_refund_values(current_session)
                )
                for line in order.lines:
                    PosOrderLineLot = self.env['pos.pack.operation.lot']
                    for pack_lot in line.pack_lot_ids:
                        PosOrderLineLot += pack_lot.copy()
                    line.copy(line._prepare_refund_data(refund_order, PosOrderLineLot))
                refund_orders |= refund_order

            return {
                'name': _('Return Products'),
                'view_mode': 'form',
                'res_model': 'pos.order',
                'res_id': refund_orders.ids[0],
                'view_id': False,
                'context': self.env.context,
                'type': 'ir.actions.act_window',
                'target': 'current',
            }
        else:
            raise UserError(_('The order cannot continue to be return'))
    
    def _prepare_adjust_data(self, company):
        origin_order = self.x_pos_order_refund_id
        # Kiểm tra xem có hóa đơn gốc không
        if not origin_order or not origin_order.sinvoice_id:
            raise UserError(_('Không tìm thấy hóa đơn gốc để điều chỉnh.'))
        self.transaction_uuid = self.pos_reference
        self.sinvoice_series = self.env.company.sinvoice_series
        general_info = {
            'templateCode': company.sinvoice_template_code,
            'invoiceSeries': company.sinvoice_series,
            # 'invoiceIssuedDate': int(refund_order.date_order.timestamp()) * 1000,
            'currencyCode': company.currency_id.name,
            'adjustmentType': '5',
            'paymentStatus': True,
            'cusGetInvoiceRight': True,
            'transactionUuid': self.pos_reference,
            'adjustedNote': 'Trả lại hàng bán',
            'adjustmentInvoiceType': '1',
            'originalInvoiceId': origin_order.sinvoice_id.id,
            'originalInvoiceIssueDate': int(origin_order.sinvoice_issued_date.timestamp()) * 1000,
        }
        # Hard code phương thức thanh toán
        payments = [
            {
                'paymentMethodName': 'TM/CK',
            }
        ]
        item_info = []
        for line in self.lines:
            # if line['price_subtotal'] < 0 or line['full_product_name'] == 'KM':
            #         continue
            if line.price_subtotal < 0 or line.full_product_name == 'KM':
                continue
            item_info.append({
                            'itemName': line.full_product_name,
                            'unitName': line.product_id.uom_id.name,
                            'unitPrice': line.price_unit,
                            'quantity': line.qty,
                            'taxPercentage': line.tax_ids_after_fiscal_position.mapped('amount') or 0.0,
                            'taxAmount': line.price_subtotal_incl - line.price_subtotal,
                            'itemTotalAmountWithoutTax': round(line.price_subtotal),
                            'itemTotalAmountWithTax': round(line.price_subtotal_incl),
                            'isIncreaseItem': False,
                            'itemNote': 'Điều chỉnh giảm số lượng',
                        })
        val = {
                'generalInvoiceInfo': general_info,
                'payments': payments,
                'itemInfo': item_info,
            }
        return val
    


        
