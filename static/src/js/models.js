odoo.define('ev_account_sinvoice.ResCompany', function (require) {
    'use strict'

    const models = require('point_of_sale.models');

    models.load_fields('res.company', ['sinvoice_search_url']);
    models.load_fields('pos.payment.method', ['is_auto_einvoice_issuance']);

    var order_model_super = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function(attr, options) {
            order_model_super.initialize.call(this,attr,options);
            this.is_get_invoice = this.is_get_invoice || false;
            this.sinvoice_data = this.sinvoice_data || {};
        },

        export_for_printing: function () {
            var receipt = order_model_super.export_for_printing.bind(this)();

            receipt = _.extend(receipt, {
                'company': _.extend(receipt.company, {
                    'sinvoice_search_url': this.pos.company.sinvoice_search_url
                })
            });
            
            receipt.is_get_invoice = this.get_is_get_invoice();
            
            // Add sinvoice data to receipt
            receipt.sinvoice_vat = this.x_sinvoice_vat || '';
            receipt.sinvoice_company_name = this.x_sinvoice_company_name || '';
            receipt.sinvoice_address = this.x_sinvoice_address || '';
            receipt.sinvoice_email = this.x_sinvoice_email || '';
            receipt.sinvoice_customer_name = this.x_sinvoice_customer_name || '';
            receipt.sinvoice_customer_email = this.x_sinvoice_customer_email || '';
            receipt.sinvoice_customer_address = this.x_sinvoice_customer_address || '';
            receipt.sinvoice_customer_id = this.x_sinvoice_customer_id || '';
            receipt.sinvoice_customer_type = this.x_sinvoice_customer_type || '';
            
            return receipt;
        },

        set_is_get_invoice: function(is_get_invoice){
            this.is_get_invoice = is_get_invoice;
        },

        get_is_get_invoice: function(){
            return this.is_get_invoice;
        },

        set_sinvoice_data: function(data){
            this.sinvoice_data = data;
            // Also set individual fields for backward compatibility
            if (data.customer_type === 'company') {
                this.x_sinvoice_vat = data.vat;
                this.x_sinvoice_company_name = data.company_name;
                this.x_sinvoice_address = data.address;
                this.x_sinvoice_email = data.email;
                this.x_sinvoice_customer_type = 'company';
            } else if (data.customer_type === 'personal') {
                this.x_sinvoice_customer_name = data.customer_name;
                this.x_sinvoice_customer_email = data.customer_email;
                this.x_sinvoice_customer_address = data.customer_address;
                this.x_sinvoice_customer_id = data.customer_id;
                this.x_sinvoice_customer_type = 'personal';
            }
            this.x_sinvoice_buyer_get_invoice = data.buyer_get_invoice;
        },

        get_sinvoice_data: function(){
            return this.sinvoice_data;
        },

        export_as_JSON: function() {
            var json = order_model_super.export_as_JSON.call(this);
            json.x_sinvoice_vat = this.x_sinvoice_vat || '';
            json.x_sinvoice_company_name = this.x_sinvoice_company_name || '';
            json.x_sinvoice_address = this.x_sinvoice_address || '';
            json.x_sinvoice_email = this.x_sinvoice_email || '';
            json.x_sinvoice_customer_name = this.x_sinvoice_customer_name || '';
            json.x_sinvoice_customer_email = this.x_sinvoice_customer_email || '';
            json.x_sinvoice_customer_address = this.x_sinvoice_customer_address || '';
            json.x_sinvoice_customer_id = this.x_sinvoice_customer_id || '';
            json.x_sinvoice_customer_type = this.x_sinvoice_customer_type || '';
            json.x_sinvoice_buyer_get_invoice = this.x_sinvoice_buyer_get_invoice || false;
            return json;
        },
    })

});