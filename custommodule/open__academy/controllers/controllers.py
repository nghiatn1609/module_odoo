# -*- coding: utf-8 -*-
from odoo import http
import werkzeug
from odoo.http import request
from odoo.addons.website.controllers.main import Website



class Main(http.Controller):
    # # kiểu json -- không chạy được
    # @http.route('/my_course/courses/json', type='json', auth='none')
    # def courses_json(self):
    #     courses = request.env['open_academy.course'].sudo().search([])
    #     return courses.read(['title'])

    # Ipx -778
    
    # # kiểu http
    @http.route('/open_academy_page',website=True, type='http', auth='public')
    def course(self):
        courses = request.env['open_academy.course'].sudo().search([])
        print("course------",courses.responsible_id)
        return request.render("open__academy.open_academy_page",{
            'course' : courses 
        })

 
    @http.route('/my_course/all-courses', type='http', auth='user')
    def all_courses(self):
        courses = request.env['open_academy.course'].sudo().search([])
        html_result = '<html><body><ul>'
        for course in courses:
            html_result += "<li> %s </li>" % course.create_uid
            html_result += "<li> %s </li>" % request.env.user.id
            
        html_result += '</ul></body></html>'
        return html_result

    @http.route('/my_course/all-courses/course-mine', type='http', auth='user')
    def all_courses_mark(self):
        courses = request.env['open_academy.course'].sudo().search([])
        html_result = '<html><body><ul>'
        for course in courses:
            if request.env['open_academy.course'].search([ ('create_uid', '=', request.env.user.id), ]):
                html_result += "<li> <ins>%s</ins> </li>" % course.title
            else:
                html_result += "<li> %s </li>" % course.title
        html_result += '</ul></body></html>'
        return html_result


    @http.route('/my_course/all-courses/mine', type='http', auth='user')
    def all_courses_mine(self):
        courses = request.env['open_academy.course'].search([ ('create_uid', '=', request.env.user.id), ])
        html_result = '<html><body><ul>'
        for course in courses:
            html_result += "<li> <ins>%s<ins> </li>" % course.title
        html_result += '</ul></body></html>'
        return html_result


class WebsiteInfo(Website): 
    @http.route('/web_info',website=True, type='http', auth='public')
    def website_info(self):
        result = super(WebsiteInfo, self).website_info()
        result.qcontext['apps'] = result.qcontext['apps'].filtered(lambda x: x.name != 'website')
        return result

# 0348623562
# class OpenAcademy(http.Controller):
#     @http.route('/open__academy/',website=True, auth='public')
#     def index(self):
#         # return "Hello, world"
#         return request.render("web.login",{})
#         # return werkzeug.utils.redirect("https://www.google.com/")

#     @http.route('/open__academy/open__academy/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('open__academy.listing', {
#             'root': '/open__academy/open__academy',
#             'objects': http.request.env['open__academy.open__academy'].search([]),
#         })

#     @http.route('/open__academy/open__academy/objects/<model("open__academy.open__academy"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('open__academy.object', {
#             'object': obj
#         })
