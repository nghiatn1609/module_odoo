# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'
    
    instructor = fields.Boolean(string="Instructor", default=False)
    
    session_ids = fields.Many2many(comodel_name='open_academy.session',string="Attendee Sessions")