# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


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
    bestTime = fields.Float(readonly=True)
    bestStyle = fields.Many2one("natacion.style", ondelete="set null")
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
    
    @api.constrains('championship')
    def _check_membership_valid(self):
        today = fields.Date.today()
        for swimmer in self:
            if not swimmer.membership_end_date or swimmer.membership_end_date < today:
                if swimmer.championship:
                    raise ValidationError(
                        "Cannot register in a championship: swimmer's membership is expired or not paid."
                    )

    
    

class style(models.Model):
    _name = "natacion.style"
    _description = "Estilo de natación"

    name = fields.Char(required=True)
    bestSwimmers = fields.One2many("res.partner", "bestStyle")
    tests = fields.One2many("natacion.test", "style_id")
    
class championship(models.Model):
    _name = "natacion.championship"
    _description = "Campeonato de natación"

    name = fields.Char(required=True)
    clubs = fields.Many2many("natacion.club")

    # Nadadores independientes añadidos manualmente
    independent_swimmers = fields.Many2many(
        "res.partner",
        string="Nadadores independientes"
    )

    # Todos los nadadores (club + independientes)
    swimmers = fields.Many2many(
        "res.partner",
        compute="_compute_swimmers",
        string="Nadadores inscritos",
        readonly=True
    )

    start_date = fields.Datetime()
    end_date = fields.Datetime()
    sessions = fields.One2many("natacion.session", "championship_id")

    @api.depends("clubs", "clubs.swimmers_list", "independent_swimmers")
    def _compute_swimmers(self):
        for record in self:
            club_swimmers = record.clubs.mapped("swimmers_list")
            record.swimmers = club_swimmers | record.independent_swimmers


            
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
    results = fields.One2many("natacion.result", "set_id", string="Resultados")

class result(models.Model):
    _name = "natacion.result"
    _description = "Resultado de un nadador en una serie"

    swimmer_id = fields.Many2one("res.partner", required=True, string="Nadador")
    test_id = fields.Many2one("natacion.test", required=True, string="Prueba")
    set_id = fields.Many2one("natacion.set", required=True, string="Serie")
    time = fields.Float(required=True, help="Tiempo en segundos")

    category_id = fields.Many2one(
        "natacion.category",
        string="Categoría",
        readonly=True
    )
    style_id = fields.Many2one(
        "natacion.style",
        string="Estilo",
        readonly=True
    )

    # Al seleccionar un test, asigna estilo y categoría automáticamente
    @api.onchange('test_id')
    def _onchange_test(self):
        for r in self:
            if r.test_id:
                r.category_id = r.test_id.category_id
                r.style_id = r.test_id.style_id
            else:
                r.category_id = False
                r.style_id = False

    # Actualiza mejor tiempo al crear
    @api.model
    def create(self, vals):
        result = super().create(vals)
        result._update_swimmer_best_time()
        return result

    # Actualiza mejor tiempo al editar
    def write(self, vals):
        res = super().write(vals)
        for record in self:
            record._update_swimmer_best_time()
        return res

    # Actualiza mejor tiempo del nadador (solo si este resultado es mejor)
    def _update_swimmer_best_time(self):
        swimmer = self.swimmer_id
        test = self.test_id
        style = test.style_id if test else False
        new_time = self.time
        
        if not swimmer.bestTime or swimmer.bestTime == 0 or new_time < swimmer.bestTime:
            swimmer.bestTime = new_time
            swimmer.bestStyle = style

    # --- NUEVO ---
    # Recalcula el mejor tiempo cuando se BORRA un resultado
    def unlink(self):
        swimmers_to_update = self.mapped("swimmer_id")

        res = super().unlink()

        for swimmer in swimmers_to_update:
            # Todos los resultados restantes del nadador
            remaining_results = self.env["natacion.result"].search([
                ("swimmer_id", "=", swimmer.id)
            ])

            if remaining_results:
                best_result = remaining_results.sorted("time")[0]
                swimmer.bestTime = best_result.time
                swimmer.bestStyle = best_result.style_id
            else:
                swimmer.bestTime = 0
                swimmer.bestStyle = False

        return res











