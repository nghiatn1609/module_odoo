# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, timedelta
from hashlib import sha256
from json import dumps

from odoo import models, api, fields
from odoo.fields import Datetime
from odoo.tools.translate import _, _lt
from odoo.exceptions import UserError


class pos_config(models.Model):
    _inherit = 'pos.config'

    release_type_sinvoice = fields.Selection(
        selection=[
            ('manual', 'Thủ công'),
            ('auto', 'Tự động'),
        ],
        string='Loại phát hành HDDT',
        default='manual',
        required=True,
        help="Select the type of release for the SInvoice.",
    )