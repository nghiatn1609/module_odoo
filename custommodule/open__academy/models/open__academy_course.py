# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api, exceptions


class Course(models.Model):
    _name = 'open_academy.course'
    _description = 'open academy Description'

    title = fields.Char(string="Title",required=True)
    description = fields.Char(string="Description")
    session_ids= fields.One2many(comodel_name='open_academy.session', inverse_name='course_id',string='Session')
    responsible_id = fields.Many2one('res.users', string="Responsible")

    _sql_constraints = [('different', 'CHECK (title <> description)', "the course description and the course title are different!"),
                        ('course_name_unique', 'unique (title)', "The name of course must be unique!")
                        ]
    # nếu muốn constraints được thực thi thì dữ liệu trước đó còn được đảm bảo đúng format của constraint chuẩn bị add
    

    
