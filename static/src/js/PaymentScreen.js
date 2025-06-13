odoo.define("ev_account_sinvoice.PaymentScreen", function (require) {
    "use strict";

    const core = require("web.core");
    const _t = core._t;
    const screens = require('point_of_sale.screens');
    const gui = require('point_of_sale.gui');
    const rpc = require("web.rpc");

    const PaymentScreenWidget = screens.PaymentScreenWidget;

    const PaymentScreenSInvoice = PaymentScreenWidget.include({
        events: _.extend({}, PaymentScreenWidget.prototype.events, {
            'change #x_sinvoice_customer_type': 'toggleCustomerFields',
            'click #x_buyer_get_invoice': '_onClickCheckedBuyerGetInvoice',
            'click .js-get-buyer-info-sinvoice': '_onClickGetBuyerInfoSInvoice',
            'click .js-confirm-tax-code': '_onClickConfirmTaxCode',
            'input input[type="text"]': '_onInputChange',
            'keydown input[type="text"]': '_onKeyDown',
            'keyup input[type="text"]': '_onKeyUp',
        }),
        
        init: function(parent, options) {
            this._super(parent, options);
            this.ready = false;
        },

        start: function() {
            var self = this;
            this._super();
            this.ready = true;
            
            // Ensure inputs are enabled after initialization
            this.$el.find('input[type="text"]').each(function() {
                $(this).prop('disabled', false);
                $(this).prop('readonly', false);
            });
        },

        show: function() {
            var self = this;
            this._super();
            // Set default display at loading
            this.$el.find(".personal-fields").show();
            this.$el.find(".company-fields").hide();
            
            // Enable all inputs
            debugger;
            this.$el.find('input[type="text"]').prop('disabled', false);
            this.$el.find('input[type="text"]').prop('readonly', false);
            
            // Add click handler to ensure inputs are enabled
            this.$el.find('input[type="text"]').on('click', function() {
                $(this).prop('disabled', false);
                $(this).prop('readonly', false);
            });
        },

        toggleCustomerFields: function(event) {
            this.customerType = event.target.value;

            if (this.customerType === "personal") {
                this._showPersonalFields();
            } else {
                this._showCompanyFields();
            }
        },

        // Hàm format chuỗi để loại bỏ khoảng trắng đầu/cuối và ký tự xuống dòng
        _formatValue: function(value) {
            if (!value) return '';
            // Loại bỏ khoảng trắng đầu/cuối và thay thế các ký tự xuống dòng bằng khoảng trắng
            return value.toString().trim().replace(/[\r\n]+/g, ' ');
        },

        _showPersonalFields: function() {
            const personalFields = this.$el.find(".personal-fields");
            const companyFields = this.$el.find(".company-fields");

            personalFields.show();
            companyFields.hide();

            // Populate fields with current customer data if available
            const customer = this.pos.get_client();
            if (customer) {
                this.$el.find("#x_sinvoice_customer_name").val(this._formatValue(customer.name));
                this.$el.find("#x_sinvoice_customer_phone").val(this._formatValue(customer.phone));
                this.$el.find("#x_sinvoice_customer_email").val(this._formatValue(customer.email));
                this.$el.find("#x_sinvoice_customer_address").val(this._formatValue(customer.street));
                this.$el.find("#x_sinvoice_customer_id").val(this._formatValue(customer.x_sinvoice_customer_id));
            }
        },

        _showCompanyFields: function() {
            const personalFields = this.$el.find(".personal-fields");
            const companyFields = this.$el.find(".company-fields");

            personalFields.hide();
            companyFields.show();
        },

        payment_input: function(input) {
            var res = this._super(input);
            
            // Check for auto einvoice when payment is made
            var paymentLines = this.pos.get_order().get_paymentlines();
            var hasAutoEinvoice = false;
            
            for (var i = 0; i < paymentLines.length; i++) {
                if (paymentLines[i].payment_method.is_auto_einvoice_issuance) {
                    hasAutoEinvoice = true;
                    break;
                }
            }
            
            if (hasAutoEinvoice) {
                this.pos.get_order().set_is_get_invoice(true);
                this.$el.find("#x_buyer_get_invoice").prop('checked', true);
                this.$el.find("#x_sinvoice").show();
            }
            
            return res;
        },

        _onClickCheckedBuyerGetInvoice: function() {
            var client = this.pos.get_client();
            if (!client) {
                this.gui.show_popup('error', {
                    'title': _t('Thông báo'),
                    'body': _t('Vui lòng chọn khách hàng để lấy hoá đơn điện tử'),
                });
                this.$el.find("#x_buyer_get_invoice").prop('checked', false);
                return;
            }
            
            var buyer_get_invoice = this.$el.find("#x_buyer_get_invoice");
            if (buyer_get_invoice.is(':checked')) {
                this.pos.get_order().set_is_get_invoice(true);
                this.$el.find("#x_sinvoice").show();
                // Gọi toggleCustomerFields với giá trị hiện tại của customer_type
                this.toggleCustomerFields({
                    target: {
                        value: this.$el.find("#x_sinvoice_customer_type").val()
                    }
                });
            } else {
                // clear data
                this.$el.find("#x_sinvoice_vat").val("");
                this.$el.find("#x_sinvoice_company_name").val("");
                this.$el.find("#x_sinvoice_address").val("");
                this.$el.find("#x_sinvoice_email").val("");

                this.pos.get_order().set_is_get_invoice(false);
                this.$el.find("#x_sinvoice").hide();
            }
        },

        _onClickGetBuyerInfoSInvoice: function() {
            var self = this;
            console.log("_onClickGetBuyerInfoSInvoice");
            let partner = this.pos.get_client();
            
            return rpc.query({
                model: "pos.order",
                method: "get_partner_info_sinvoice",
                args: ["", partner.id.toString()],
            }).then(function(data) {
                console.log(data);
                if (data !== undefined) {
                    self.$el.find("#x_sinvoice_vat").val(self._formatValue(data["sinvoice_vat"]));
                    self.$el.find("#x_sinvoice_company_name").val(self._formatValue(data["sinvoice_company_name"]));
                    self.$el.find("#x_sinvoice_address").val(self._formatValue(data["sinvoice_address"]));
                    self.$el.find("#x_sinvoice_email").val(self._formatValue(data["sinvoice_email"]));
                } else {
                    self.gui.show_popup('error', {
                        'title': _t('Thông báo'),
                        'body': _t('Không tìm thấy thông tin lấy hoá đơn gần nhất.'),
                    });
                    return;
                }
            });
        },

        _onClickConfirmTaxCode: function() {
            var self = this;
            console.log("_onClickConfirmTaxCode");
            let x_sinvoice_vat = this.$el.find("#x_sinvoice_vat");
            let x_sinvoice_company_name = this.$el.find("#x_sinvoice_company_name");
            let x_sinvoice_address = this.$el.find("#x_sinvoice_address");
            let x_sinvoice_email = this.$el.find("#x_sinvoice_email");
            let url_check_vat = "url_check_vat";
            
            if (x_sinvoice_vat.val().trim()) {
                rpc.query({
                    model: "account.sinvoice",
                    method: "get_url_check_vat",
                    args: [null],
                }).then(function(res) {
                    if (res) {
                        url_check_vat = res;
                        let url = url_check_vat + x_sinvoice_vat.val().toString().trim();
                        $.ajax({
                            type: "GET",
                            url: url,
                            async: false,
                            success: function(response) {
                                if (response["code"] !== "00") {
                                    x_sinvoice_company_name.val("");
                                    x_sinvoice_address.val("");
                                    x_sinvoice_email.val("");
                                    self.gui.show_popup('error', {
                                        'title': _t('Thông báo'),
                                        'body': _t(response["desc"]),
                                    });
                                    return;
                                }
                                x_sinvoice_company_name.val(response["data"]["name"]);
                                x_sinvoice_address.val(response["data"]["address"]);
                                return;
                            },
                            error: function(err) {
                                self.gui.show_popup('error', {
                                    'title': _t('Thông báo'),
                                    'body': _t(err),
                                });
                                return;
                            },
                            timeout: 10000,
                        });
                    } else {
                        self.gui.show_popup('error', {
                            'title': _t('Thông báo'),
                            'body': _t('Không tìm thấy URL kiểm tra mã số thuế.'),
                        });
                        return;
                    }
                });
            } else {
                self.gui.show_popup('error', {
                    'title': _t('Thông báo'),
                    'body': _t('Vui lòng nhập mã số thuế để kiểm tra.'),
                });
                return;
            }
        },

        finalize_validation: function() {
            var self = this;
            if (this.pos.get_order().get_is_get_invoice()) {
                // Get customer type
                var customerType = this.$el.find("#x_sinvoice_customer_type").val();
                
                if (customerType === 'company') {
                    // Company validation
                    var x_sinvoice_vat = this.$el.find("#x_sinvoice_vat").val().trim();
                    var x_sinvoice_company_name = this.$el.find("#x_sinvoice_company_name").val().trim();
                    var x_sinvoice_address = this.$el.find("#x_sinvoice_address").val().trim();
                    var x_sinvoice_email = this.$el.find("#x_sinvoice_email").val().trim();

                    if (!x_sinvoice_vat) {
                        self.gui.show_popup('error', {
                            'title': _t('Thông báo'),
                            'body': _t('Vui lòng nhập mã số thuế.'),
                        });
                        return;
                    }
                    if (!x_sinvoice_company_name) {
                        self.gui.show_popup('error', {
                            'title': _t('Thông báo'),
                            'body': _t('Vui lòng nhập tên công ty.'),
                        });
                        return;
                    }

                    // Set company data to order
                    this.pos.get_order().set_sinvoice_data({
                        customer_type: 'company',
                        vat: x_sinvoice_vat,
                        company_name: x_sinvoice_company_name,
                        address: x_sinvoice_address,
                        email: x_sinvoice_email,
                        buyer_get_invoice: true
                    });
                } else {
                    // Personal validation
                    var x_sinvoice_customer_name = this.$el.find("#x_sinvoice_customer_name").val().trim();
                    var x_sinvoice_customer_email = this.$el.find("#x_sinvoice_customer_email").val().trim();
                    var x_sinvoice_customer_address = this.$el.find("#x_sinvoice_customer_address").val().trim();
                    var x_sinvoice_customer_id = this.$el.find("#x_sinvoice_customer_id").val().trim();

                    if (!x_sinvoice_customer_name) {
                        self.gui.show_popup('error', {
                            'title': _t('Thông báo'),
                            'body': _t('Vui lòng nhập họ và tên.'),
                        });
                        return;
                    }

                    // Set personal data to order
                    this.pos.get_order().set_sinvoice_data({
                        customer_type: 'personal',
                        customer_name: x_sinvoice_customer_name,
                        customer_email: x_sinvoice_customer_email,
                        customer_address: x_sinvoice_customer_address,
                        customer_id: x_sinvoice_customer_id,
                        buyer_get_invoice: true
                    });
                }
            }

            return this._super();
        },

        _onInputChange: function(event) {
            // Ensure input is enabled
            $(event.target).prop('disabled', false);
            $(event.target).prop('readonly', false);
        },

        _onKeyDown: function(event) {
            // Ensure input is enabled
            $(event.target).prop('disabled', false);
            $(event.target).prop('readonly', false);
        },

        _onKeyUp: function(event) {
            // Ensure input is enabled
            $(event.target).prop('disabled', false);
            $(event.target).prop('readonly', false);
        },
    });

    return PaymentScreenSInvoice;
});
