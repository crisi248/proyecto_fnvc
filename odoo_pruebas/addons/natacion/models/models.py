# -*- coding: utf-8 -*-

from datetime import date
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
    points = fields.Integer(readonly=True)
    ribbon_color = fields.Char(compute="_compute_ribbon_color", string="Color del Ribbon", readonly=True)
    medal = fields.Char(compute="_compute_medal", string="Medal Emoji", readonly=True)
    ranking = fields.Integer(compute="_compute_ranking", string="Ranking", readonly=True)

    @api.depends('points')
    def _compute_ranking(self):
        for club in self:
            if club.ranking is None: 
                club.ranking = 9999 
        
        clubs = self.env["natacion.club"].search([('points', '>', 0)], order="points desc")
        
        for index, club in enumerate(clubs, 1):
            club.ranking = index

    @api.depends('ranking')
    def _compute_medal(self):
        for club in self:
            if club.ranking == 1:
                club.medal = "🥇"
            elif club.ranking == 2:
                club.medal = "🥈" 
            elif club.ranking == 3:
                club.medal = "🥉" 
            else:
                club.medal = ""

    @api.depends('ranking')
    def _compute_ribbon_color(self):
        for club in self:
            if club.ranking == 1:
                club.ribbon_color = "#FFD700"
            elif club.ranking == 2:
                club.ribbon_color = "#C0C0C0"
            elif club.ranking == 3:
                club.ribbon_color = "#cd7f32"
            else:
                club.ribbon_color = "transparent" 


class category(models.Model):
    _name = "natacion.category"
    _description = "Categoria"

    name = fields.Char(required=True)
    minAge = fields.Integer()
    maxAge = fields.Integer()
    swimmers_list = fields.One2many("res.partner", "category")
    tests = fields.One2many("natacion.test", "category_id")

    @api.constrains("minAge", "maxAge")
    def _check_age_range(self):
        for rec in self:
            if rec.minAge and rec.maxAge and rec.minAge > rec.maxAge:
                raise ValidationError("La edad mínima no puede ser mayor que la edad máxima.")

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

    independent_swimmers = fields.Many2many(
        "res.partner",
        compute="_compute_independent_swimmers",
        store=True,
        readonly=True,
        string="Nadadores independientes"
    )

    swimmers = fields.Many2many(
        "res.partner",
        compute="_compute_swimmers",
        string="Nadadores inscritos",
        readonly=True
    )

    start_date = fields.Datetime(required=True)
    end_date = fields.Datetime()
    sessions = fields.One2many("natacion.session", "championship_id", ondelete="cascade")

    @api.depends("sessions.swimmers")
    def _compute_independent_swimmers(self):
        for record in self:
            swimmers = record.sessions.mapped("swimmers")
            record.independent_swimmers = swimmers


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
    sessionTime = fields.Integer(compute="_compute_sessionTime", store=True, readonly=True)
    championship_id = fields.Many2one("natacion.championship", ondelete="set null")
    tests = fields.One2many("natacion.test", "session_id", ondelete="cascade")
    swimmers = fields.Many2many(
    "res.partner",
    compute="_compute_swimmers",
    store=True,
    readonly=True)

    @api.depends("tests.swimmers")
    def _compute_swimmers(self):
        for record in self:
            swimmers = record.tests.mapped("swimmers")
            record.swimmers = swimmers

    @api.depends("tests.timeTest")
    def _compute_sessionTime(self):
        for record in self:
            total = 0
            for test in record.tests:
                total += test.timeTest
            record.sessionTime = total

    @api.constrains("date", "championship_id")
    def _check_session_date(self):
        for record in self:
            if not record.championship_id or not record.date:
                continue

            start = record.championship_id.start_date
            end = record.championship_id.end_date
            session_date = record.date

            if session_date < start:
                raise ValidationError(
                    "La fecha de la sesión (%s) no puede ser anterior "
                    "al inicio del campeonato (%s)." % (session_date, start)
                )

            if end and session_date > end:
                raise ValidationError(
                    "La fecha de la sesión (%s) no puede ser posterior "
                    "al final del campeonato (%s)." % (session_date, end)
                )
            
            for s in record.championship_id.sessions:
                if s.id != record.id:
                    if s.date == session_date:
                        raise ValidationError(
                            "Ya existe otra sesión en este campeonato con la misma fecha (%s)." % session_date
                        )

class test(models.Model):
    _name = "natacion.test"
    _description = "Test de natación"

    name = fields.Char(required=True)
    description = fields.Char()
    style_id = fields.Many2one("natacion.style", ondelete="set null")
    category_id = fields.Many2one("natacion.category", ondelete="set null")
    swimmers = fields.Many2many("res.partner",compute="_compute_swimmers",store=True,readonly=True)
    sets = fields.One2many("natacion.set", "test_id", ondelete="cascade")
    session_id = fields.Many2one("natacion.session")
    timeTest = fields.Integer(compute="_compute_timeTest", store=True, readonly=True)

    @api.depends("sets.results.swimmer_id")
    def _compute_swimmers(self):
        for record in self:
            swimmers = record.sets.mapped("results.swimmer_id")
            record.swimmers = swimmers

    @api.depends("sets")
    def _compute_timeTest(self):
        for record in self:
            record.timeTest = len(record.sets) * 10

class set(models.Model):
    _name = "natacion.set"
    _description = "Set de natación"

    name = fields.Char(required=True)
    test_id = fields.Many2one("natacion.test", ondelete="cascade")
    results = fields.One2many("natacion.result", "set_id", string="Resultados")

class result(models.Model):
    _name = "natacion.result"
    _description = "Resultado de un nadador en una serie"

    swimmer_id = fields.Many2one(
        "res.partner",
        required=True,
        string="Nadador"
    )

    set_id = fields.Many2one(
        "natacion.set",
        required=True,
        string="Serie",
        ondelete="cascade"
    )

    test_id = fields.Many2one(
        "natacion.test",
        string="Prueba",
        related="set_id.test_id",
        store=True,
        readonly=True
    )

    time = fields.Float(
        required=True,
        help="Tiempo en segundos"
    )

    category_id = fields.Many2one(
        "natacion.category",
        string="Categoría",
        related="test_id.category_id",
        store=True,
        readonly=True
    )

    style_id = fields.Many2one(
        "natacion.style",
        string="Estilo",
        related="test_id.style_id",
        store=True,
        readonly=True
    )

    @api.model
    def create(self, vals):
        result = super().create(vals)
        result._update_swimmer_best_time()
        result._update_club_points()
        return result

    def write(self, vals):
        res = super().write(vals)
        for record in self:
            record._update_swimmer_best_time()
            record._update_club_points()
        return res

    def _update_swimmer_best_time(self):
        swimmer = self.swimmer_id
        test = self.test_id
        style = test.style_id if test else False
        new_time = self.time

        if not swimmer.bestTime or swimmer.bestTime == 0 or new_time < swimmer.bestTime:
            swimmer.bestTime = new_time
            swimmer.bestStyle = style

    def _update_club_points(self):
        swimmer = self.swimmer_id
        if swimmer.club:
            if self.time == 0:
                return

            if self.time <= 10:
                points = 100
            elif self.time <= 30:
                points = max(0, 100 - ((self.time - 10) * 3.33))
            else:
                points = 0

            swimmer.club.points = swimmer.club.points + int(points)

    def unlink(self):
        swimmers_to_update = self.mapped("swimmer_id")
        res = super().unlink()

        for swimmer in swimmers_to_update:
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



class RegisterSwimmerWizard(models.TransientModel):
    _name = "natacion.register.swimmer.wizard"
    _description = "Wizard de inscripción de nadadores"

    championship_id = fields.Many2one(
        "natacion.championship",
        required=True,
        readonly=True
    )

    swimmer_id = fields.Many2one(
        "res.partner",
        required=True,
        domain="[('is_swimmer', '=', True)]",
        string="Nadador"
    )

    membership_ok = fields.Boolean(
        compute="_compute_membership_ok",
        string="Cuota pagada"
    )

    @api.depends("swimmer_id")
    def _compute_membership_ok(self):
        today = date.today()
        for w in self:
            w.membership_ok = bool(
                w.swimmer_id.membership_end_date
                and w.swimmer_id.membership_end_date >= today
            )

    @api.onchange("swimmer_id")
    def _onchange_swimmer(self):
        if self.swimmer_id and not self.membership_ok:
            return {
                "warning": {
                    "title": "Cuota no pagada",
                    "message": "Este nadador no tiene la cuota anual pagada."
                }
            }

    def action_confirm(self):
        self.ensure_one()

        if not self.membership_ok:
            raise UserError("No se puede inscribir un nadador sin la cuota pagada.")

        championship = self.championship_id

        # Evitar duplicados
        if self.swimmer_id in championship.swimmers:
            raise UserError("Este nadador ya está inscrito en el campeonato.")

        # Añadir como nadador independiente
        championship.independent_swimmers = [(4, self.swimmer_id.id)]