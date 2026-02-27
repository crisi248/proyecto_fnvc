# -*- coding: utf-8 -*-

from odoo import models, fields, api


class skills_repaso(models.Model):
#     _name = 'skills_repaso.skills_repaso'
#     _description = 'skills_repaso.skills_repaso'
    _inherit = 'hr.skill'

    description = fields.Html()

