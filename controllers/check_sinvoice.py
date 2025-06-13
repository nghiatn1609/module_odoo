from odoo import http
from odoo.http import request, Response

class CheckSinvoiceController(http.Controller):
    @http.route('/check/sinvoice', type='json', auth='public', methods=['POST'], csrf=False)
    def lookup_invoice(self):
        params = request.jsonrequest
        order_ref = params.get('pos_reference')
        phone = params.get('phone')
        partner = request.env['res.partner'].sudo().search([
            ('phone', '=', phone)
        ], limit=1)
        order = request.env['pos.order'].sudo().search([
            ('pos_reference', '=', order_ref),
            ('partner_id', '=', partner.id)
        ], limit=1)

        if not order:
            return {'status': 'Not found', 
                    'message': 'Không tìm thấy thông tin trên hệ thống. Vui lòng kiểm tra lại và nhập đúng mã tra cứu và số điện thoại mua hàng.'}

        if not order.sinvoice_state or order.sinvoice_state == 'no_release':
            return {
                'status': 'Not issued',
                'message': 'Đơn hàng của quý khách chưa được xuất hoá đơn.',
                'data': {
                    'pos_reference': order.pos_reference,
                    'date_order': order.date_order,
                }
            }

        if order.sinvoice_state == 'released':
            return {
                'status': 'Issued',
                'message': 'Đã phát hành hoá đơn.',
                'data': {
                    'pos_reference': order.pos_reference,
                    'date_order': order.date_order,
                    'Sinvoice_no': order.sinvoice_no,
                    'issued_date': order.sinvoice_issued_date,
                    'reservation_code': order.sinvoice_id.reservation_code,
                }
            }
