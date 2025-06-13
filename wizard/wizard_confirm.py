from odoo import fields, models, _
from odoo.exceptions import UserError


class WizardConfirmExportEinvoice(models.TransientModel):
    _name = 'wizard.confirm.export.einvoice'
    _description = 'wizard.confirm.export.einvoice'

    def button_confirm(self):
        active_ids = self._context.get('active_ids')
        active_model = self._context.get('active_model')
        pos_order_ids = self.env[active_model].search([('id', 'in', active_ids)])
        if pos_order_ids:
            lot_series = []
            # Loại bỏ đơn trả hàng và các đơn gốc đã trả full
            orders = pos_order_ids.search(
                [('id', 'in', active_ids),('amount_total', '>', 0), ('x_pos_order_refund_id', '=', False),('sinvoice_id','=',False)])
                # [('id', 'in', active_ids),('amount_total', '>', 0), ('x_pos_order_refund_id', '=', False),('sinvoice_id','=',False),('x_refund_all', '=', False)])
            orders_return = pos_order_ids.search([('id', 'in', active_ids),('x_pos_order_refund_id', '!=', False)]).mapped('x_pos_order_refund_id')

            orders_release = orders - orders_return

            lens = len(orders_release)
            number_per_lot = self.env.company.number_pos_per_lot
            lot_qty = lens // number_per_lot
            j = lot_qty
            i = 0
            while j > 0:
                lot_series.append(orders_release[i:i + number_per_lot])
                i += number_per_lot
                j -= 1
                lens -= number_per_lot
            if lens > 0:
                lot_series.append(orders_release[lot_qty * number_per_lot:])
            for item in lot_series:
                val = {
                    'action_type': 'release',
                    'line_ids': item
                }
                sinvoice_lot = self.env['create.sinvoice.lot'].sudo().create(val)
                sinvoice_lot.action_api_release_sinvoice()