# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api, exceptions

    
class session(models.Model):
    _name = 'open_academy.session'
    _description = 'open_academy Session'
    
    name = fields.Char(string="Name", required=True)
    start_date = fields.Date(default=fields.Date.today)
    course_id = fields.Many2one(comodel_name="open_academy.course",string="Course", required=True)
    # start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6,2), help="Duration in days", translate=True)
    seats = fields.Integer(string="Number of seats")
    instructor_id = fields.Many2one('res.partner', string="Instructor")
    attendees_ids = fields.Many2many(comodel_name='res.partner', string='Attendees')
    taken_seats = fields.Float(string="Taken seats", compute ="_taken_seats")
    active = fields.Boolean(default = True)
    date_end = fields.Date(string="End date", store=True ,compute='_get_end_date', inverse='_set_end_date')
    attendees_count = fields.Integer(
        string="Attendees count", compute='_get_attendees_count', store=True)
    color = fields.Integer()
    

    
    # def _get_report_values(self, docids, data=None):
    #     # get the report action back as we will need its data
    #     report = self.env['ir.actions.report']._get_report_from_name('module.report_name')
    #     # get the records selected for this rendering of the report
    #     obj = self.env[report.model].browse(docids)
    #     # return a custom rendering context
    #     return {
    #         'lines': docids.get_lines()
    #     }
    
    def action_cf(self):
        for r in self:
            val = {
                'name': 'tre',
                'course_id': '4',
                'duration' : '50',
                'seats' : '90',
            }
            self.env['open_academy.session'].create(val)
            re = self.env['open_academy.session'].search([])
            print("display name........", re)
            # print("display name...", re.display_name)
            # print("hekdfg-----------------hfdigugue--------------reu")
    
    @api.depends('attendees_ids','seats')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0
            else:
                r.taken_seats = 100 * len(r.attendees_ids) / r.seats
            print("taken_depend")
                
    @api.depends('attendees_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendees_ids)
    
    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.date_end = r.start_date
                continue
            
            duration = timedelta(days=r.duration)
            r.date_end = r.start_date + duration
            
               
    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.date_end):
                continue

            r.duration = (r.date_end - r.start_date).days
     
    # khi bấm create, và chỉnh sửa dữ liệu nhưng chưa lưu vào database thì onchange hoạt động
    # @api.onchange('course_id')
    # def _onchange_name(self):
    #     if self.course_id:
    #         if self.course_id.title:
    #             self.name = self.course_id.title
    #             print("trigger")
        # self.seats = '90'
    
    @api.onchange('seats', 'attendees_ids')
    def _verify_valid_seats(self):
        # if self.seats < 0:
        #     print("onchange triggered")
        #     return {
        #         'warning': {
        #         'title': "Incorrect 'seats' value",
        #         'message': "The number of available seats may not be negative",
        #         },
        #     }    
        if self.seats < len(self.attendees_ids):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees",
                },     
            }
            
    # vẫn chưa sửa được việc: "khi create/edit giá trị sai nhưng mà dữ liệu sai đó vẫn lưu vào database"

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendees_ids:
                raise exceptions.ValidationError("A session's instructor can't be an attendee")
            
    @api.constrains('name')
    def _constrains_name(self):
        for r in self:
            if r.name == "fpt":
                raise exceptions.ValidationError("NOT FPT")