# -*- coding: utf-8 -*-

from odoo import models, fields, api

class club(models.Model):
    _name = "natacion.club"
    _description = "Club de natación"

    name = fields.Char(required=True)
    town = fields.Char()
    swimmers_list = fields.One2many("natacion.swimmer", "club")
    championships = fields.Many2many("natacion.championship")


class category(models.Model):
    _name = "natacion.category"
    _description = "Categoria"

    name = fields.Char(required=True)
    minAge = fields.Integer()
    maxAge = fields.Integer()
    swimmers_list = fields.One2many("natacion.swimmer", "category_id")
    tests = fields.One2many("natacion.test", "category_id")

class swimmer(models.Model):
    _name = "natacion.swimmer"
    _description = "Nadador"

    name = fields.Char(required=True)
    image = fields.Image()
    club = fields.Many2one("natacion.club", ondelete="set null")
    yearOfBirth = fields.Integer()
    age = fields.Integer(compute="_get_age")
    category_id = fields.Many2one("natacion.category", ondelete="set null")
    bestTime = fields.Float()
    bestStyle = fields.One2many("natacion.style", "bestSwimmers")
    sessions = fields.Many2many("natacion.session")
    tests = fields.Many2many("natacion.test")
    championship = fields.Many2many("natacion.championship")

    @api.depends("yearOfBirth")
    def _get_age(self):
        for s in self:
            s.age = int(fields.Date.to_string(fields.Date.today()).split('-')[0]) - s.yearOfBirth

class style(models.Model):
    _name = "natacion.style"
    _description = "Estilo de natación"

    name = fields.Char(required=True)
    bestSwimmers = fields.Many2one("natacion.swimmer", ondelete="set null")
    tests = fields.One2many("natacion.test", "style_id")
    
class championship(models.Model):
    _name = "natacion.championship"
    _description = "Campeonato de natación"

    name = fields.Char(required=True)
    clubs = fields.Many2many("natacion.club")
    # Nadadores inscritos de un club que esta inscrito
    swimmers = fields.Many2many("natacion.swimmer", readonly=True, compute="_compute_swimmers")
    start_date = fields.Datetime()
    end_date = fields.Datetime()
    sessions = fields.One2many("natacion.session", "championship_id")

    @api.depends("clubs", "clubs.swimmers_list")
    def _compute_swimmers(self):
        for record in self:
            all_swimmers = record.clubs.mapped("swimmers_list")
            record.swimmers = all_swimmers
            
class session(models.Model):
    _name = "natacion.session"
    _description = "Sesión de natación"

    name = fields.Char(required=True)
    date = fields.Datetime()
    championship_id = fields.Many2one("natacion.championship", ondelete="set null")
    tests = fields.One2many("natacion.test", "session_id")
    swimmers = fields.Many2many("natacion.swimmer")

class test(models.Model):
    _name = "natacion.test"
    _description = "Test de natación"

    name = fields.Char(required=True)
    description = fields.Char(required=True)
    style_id = fields.Many2one("natacion.style", ondelete="set null")
    category_id = fields.Many2one("natacion.category", ondelete="set null")
    swimmers = fields.Many2many("natacion.swimmer")
    sets = fields.One2many("natacion.set", "test_id")
    session_id = fields.Many2one("natacion.session", ondelete="set null")

class set(models.Model):
    _name = "natacion.set"
    _description = "Set de natación"

    name = fields.Char(required=True)
    test_id = fields.Many2one("natacion.test", ondelete="set null")







