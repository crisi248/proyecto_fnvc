# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Club(models.Model):
    _name = "natacion.club"
    _description = "Club de natación"

    name = fields.Char(required=True)
    town = fields.Char()
    image = fields.Image()
    swimmers_list = fields.One2many(
        "res.partner",
        "club", 
        string="Nadadores"
    )
    championships = fields.Many2many("natacion.championship")



class category(models.Model):
    _name = "natacion.category"
    _description = "Categoria"

    name = fields.Char(required=True)
    minAge = fields.Integer()
    maxAge = fields.Integer()
    swimmers_list = fields.One2many("res.partner", "category")
    tests = fields.One2many("natacion.test", "category_id")



class swimmer(models.Model):
    #_name = "natacion.swimmer"
    #_description = "Nadador"
    _inherit = "res.partner"

    #name = fields.Char(required=True)
    is_swimmer = fields.Boolean()
    image = fields.Image()
    club = fields.Many2one("natacion.club", ondelete="set null")
    yearOfBirth = fields.Integer()
    age = fields.Integer(compute="_get_age")
    category = fields.Many2one("natacion.category", ondelete="set null")
    bestTime = fields.Float()
    bestStyle = fields.One2many("natacion.style", "bestSwimmers")
    sessions = fields.Many2many("natacion.session")
    tests = fields.Many2many("natacion.test")
    championship = fields.Many2many("natacion.championship")
    membership_end_date = fields.Date(readonly=True)
    membership_progress = fields.Integer(compute="_compute_service_progress")

    def _compute_service_progress(self):
        for s in self:
            if not s.membership_end_date:
                s.membership_progress = 0
                continue

            today = fields.Date.from_string(fields.Date.today())
            end = fields.Date.from_string(s.membership_end_date)

            start = end.replace(year=end.year - 1)

            if today >= end:
                s.membership_progress = 100
                continue

            total = (end - start).days or 1
            used = (today - start).days

            s.membership_progress = min(100, max(0, int((used / total) * 100)))


    @api.depends("yearOfBirth")
    def _get_age(self):
        for s in self:
            s.age = int(fields.Date.to_string(fields.Date.today()).split('-')[0]) - s.yearOfBirth
    
    def formulario_completo(self):
        return {
            "name" : "Swimmer",
            "view_type" : "form",
            "view_mode" : "form",
            "res_model" : "res.partner",
            "res_id" : self.id,
            "type" : "ir.actions.act_window",
            "target" : "current",
        }
    
    def pagar_cuota(self):

        product = self.env.ref("natacion.product_cuota_anual")

        start_date = fields.Date.today()

        end_dt = fields.Date.from_string(start_date)
        end_dt = end_dt.replace(year=end_dt.year + 1)

        order = self.env["sale.order"].create({
            "partner_id": self.id,
            "validity_date": end_dt,
        })

        self.env["sale.order.line"].create({
        "order_id": order.id,
        "product_id": product.id,
        })

        self.membership_end_date = end_dt

        return order.get_formview_action()
    
    

class style(models.Model):
    _name = "natacion.style"
    _description = "Estilo de natación"

    name = fields.Char(required=True)
    bestSwimmers = fields.Many2one("res.partner", ondelete="set null")
    tests = fields.One2many("natacion.test", "style_id")
    
class championship(models.Model):
    _name = "natacion.championship"
    _description = "Campeonato de natación"

    name = fields.Char(required=True)
    clubs = fields.Many2many("natacion.club")
    # Nadadores inscritos de un club que esta inscrito
    swimmers = fields.Many2many("res.partner", readonly=True, compute="_compute_swimmers")
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
    swimmers = fields.Many2many("res.partner")

class test(models.Model):
    _name = "natacion.test"
    _description = "Test de natación"

    name = fields.Char(required=True)
    description = fields.Char(required=True)
    style_id = fields.Many2one("natacion.style", ondelete="set null")
    category_id = fields.Many2one("natacion.category", ondelete="set null")
    swimmers = fields.Many2many("res.partner")
    sets = fields.One2many("natacion.set", "test_id")
    session_id = fields.Many2one("natacion.session", ondelete="set null")

class set(models.Model):
    _name = "natacion.set"
    _description = "Set de natación"

    name = fields.Char(required=True)
    test_id = fields.Many2one("natacion.test", ondelete="set null")







