# -*- coding: utf-8 -*-

from odoo import models, fields, api

class club(models.Model):
    _name = "natacion.club"
    _description = "Club de natación"

    name = fields.Char(required=True)
    town = fields.Char()
    partner = fields.Char()

class category(models.Model):
    _name = "natacion.category"
    _description = "Categoria"

    name = fields.Char(required=True)
    minAge = fields.Integer()
    maxAge = fields.Integer()
    swimmers_list = fields.One2many("natacion.swimmer", "category_id")

class swimmer(models.Model):
    _name = "natacion.swimmer"
    _description = "Nadador"

    name = fields.Char(required=True)
    yearOfBirth = fields.Char()
    age = fields.Integer()
    category_id = fields.Many2one("natacion.category", ondelete="set null")
    bestTime = fields.Float(related='style.bestTime')

class style(models.Model):
    _name = "natacion.swimmer"
    _description = "Nadador"

    name = fields.Char(required=True)





