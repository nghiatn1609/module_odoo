odoo.define('ev_account_sinvoice.models', function (require) {
    'use strict'

    let models = require('point_of_sale.models')

    let order = models.Order
    models.Order = models.Order.extend({
        initialize: function (attributes, options) {
            this.x_sinvoice_vat = options.x_sinvoice_vat || ''
            this.x_sinvoice_company_name = options.x_sinvoice_company_name || ''
            this.x_sinvoice_address = options.x_sinvoice_address || ''
            this.x_sinvoice_email = options.x_sinvoice_email || ''
            
            // Thêm các trường mới
            this.x_sinvoice_buyer_get_invoice = options.x_sinvoice_buyer_get_invoice || false
            this.x_sinvoice_customer_type = options.x_sinvoice_customer_type || 'personal'
            this.x_sinvoice_customer_name = options.x_sinvoice_customer_name || ''
            this.x_sinvoice_customer_id = options.x_sinvoice_customer_id || ''
            
            order.prototype.initialize.apply(this, arguments)
            return this
        },

        init_from_JSON: function (json) {
            this.x_sinvoice_vat = json.x_sinvoice_vat
            this.x_sinvoice_company_name = json.x_sinvoice_company_name
            this.x_sinvoice_address = json.x_sinvoice_address
            this.x_sinvoice_email = json.x_sinvoice_email
            
            // Thêm các trường mới
            this.x_sinvoice_buyer_get_invoice = json.x_sinvoice_buyer_get_invoice
            this.x_sinvoice_customer_type = json.x_sinvoice_customer_type
            this.x_sinvoice_customer_name = json.x_sinvoice_customer_name
            this.x_sinvoice_customer_id = json.x_sinvoice_customer_id || ''
            
            order.prototype.init_from_JSON.call(this, json)
        },

        export_as_JSON: function () {
            let json = order.prototype.export_as_JSON.apply(this, arguments)
            json.x_sinvoice_vat = this.get_x_sinvoice_vat()
            json.x_sinvoice_company_name = this.get_x_sinvoice_company_name()
            json.x_sinvoice_address = this.get_x_sinvoice_address()
            json.x_sinvoice_email = this.get_x_sinvoice_email()
            
            // Thêm các trường mới
            json.x_sinvoice_buyer_get_invoice = this.get_is_get_invoice()
            json.x_sinvoice_customer_type = this.get_x_sinvoice_customer_type()
            json.x_sinvoice_customer_name = this.get_x_sinvoice_customer_name()
            json.x_sinvoice_customer_id = this.get_x_sinvoice_customer_id()
            
            return json
        },
        
        get_x_sinvoice_vat: function () {
            return this.x_sinvoice_vat
        },
        get_x_sinvoice_company_name: function () {
            return this.x_sinvoice_company_name
        },
        get_x_sinvoice_address: function () {
            return this.x_sinvoice_address
        },
        get_x_sinvoice_email: function () {
            return this.x_sinvoice_email
        },
        
        get_is_get_invoice: function () {
            return this.is_get_invoice || this.x_sinvoice_buyer_get_invoice || false
        },
        set_is_get_invoice: function (value) {
            this.is_get_invoice = value;
            this.x_sinvoice_buyer_get_invoice = value;
        },
        get_x_sinvoice_customer_type: function () {
            return this.x_sinvoice_customer_type
        },
        get_x_sinvoice_customer_name: function () {
            return this.x_sinvoice_customer_name
        },
        get_x_sinvoice_customer_id: function () {
            return this.x_sinvoice_customer_id
        }
    })
})