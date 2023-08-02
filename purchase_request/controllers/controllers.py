# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class OderProduct(http.Controller):
    # @http.route('/purchase_request', auth='public')
    # def index(self, **kw):
    #     return "Hello, world"

    @http.route('/purchase_request', auth='public', type='http',website=True)
    def purchase_request(self):
        patients = request.env['purchase.request'].sudo().search([])
        print("patients---------",patients.request_id)
        # print("patients---------",user.id)
        return  "Hello, world"





#     @http.route('/oder_product/oder_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('oder_product.listing', {
#             'root': '/oder_product/oder_product',
#             'objects': http.request.env['oder_product.oder_product'].search([]),
#         })

#     @http.route('/oder_product/oder_product/objects/<model("oder_product.oder_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('oder_product.object', {
#             'object': obj
#         })
