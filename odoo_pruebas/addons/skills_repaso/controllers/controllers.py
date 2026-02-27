# -*- coding: utf-8 -*-
# from odoo import http


# class SkillsRepaso(http.Controller):
#     @http.route('/skills_repaso/skills_repaso', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/skills_repaso/skills_repaso/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('skills_repaso.listing', {
#             'root': '/skills_repaso/skills_repaso',
#             'objects': http.request.env['skills_repaso.skills_repaso'].search([]),
#         })

#     @http.route('/skills_repaso/skills_repaso/objects/<model("skills_repaso.skills_repaso"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('skills_repaso.object', {
#             'object': obj
#         })

