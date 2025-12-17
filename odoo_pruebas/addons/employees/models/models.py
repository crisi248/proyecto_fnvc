# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class nomina(models.Model):
    _name = 'employees.nomina'
    _description = 'employees.nomina'


    estado = fields.Char(default="Sin pagar", readonly=True)
    total_salario = fields.Integer()
    fecha_inicio = fields.Date()
    fecha_fin = fields.Date()
    id_empleado = fields.Many2one("hr.employee", ondelete="set null")
    conceptos = fields.Many2many("employees.concepto")

    @api.constrains('fecha_inicio', 'fecha_fin')
    def _check_fecha_nacimiento(self):
        for record in self:
            if record.fecha_inicio > record.fecha_fin:
                raise ValidationError("ERROR: Fecha de inicio inválida")
            
    def concepto_basico(self):

        concepto = self.env["employees.concepto"].create({
            "tipo": "Salario base",
            "name": "Salario base",
            "nominas": self,
        })

class empleado(models.Model):
    _inherit = "hr.employee"

    tipo_contrato = fields.Char()
    salario_base = fields.Integer()
    nomina = fields.One2many("employees.nomina", "id_empleado")

class concepto(models.Model):
    _name = 'employees.concepto'
    _description = 'employees.concepto'
    
    name = fields.Char()
    tipo = fields.Char()
    nominas = fields.Many2many("employees.nomina")








