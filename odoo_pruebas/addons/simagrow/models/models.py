# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Usuario(models.Model):
    _name = 'simagrow.usuario'
    _description = 'Usuario de Simagrow'

    nif = fields.Char(required=True)
    nombre = fields.Char(required=True)
    apellidos = fields.Char(required=True)
    fecha_nacimiento = fields.Date(required=True)
    correo = fields.Char(required=True)
    creditos = fields.Integer(readonly=True)
    num_incidencias = fields.Integer(string="Número de incidencias", readonly=True, default=0)

    incidencia_ids = fields.One2many('simagrow.incidencia', 'usuario_id', string="Incidencias")

    name = fields.Char(string="Nombre completo", compute="_compute_name")

    @api.depends('nombre', 'apellidos')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.nombre} {record.apellidos}"

    @api.constrains('fecha_nacimiento')
    def _check_fecha_nacimiento(self):
        for record in self:
            if record.fecha_nacimiento and record.fecha_nacimiento > fields.Date.today():
                raise ValidationError("La fecha de nacimiento no puede ser futura.")


class Incidencia(models.Model):
    _name = 'simagrow.incidencia'
    _description = 'Incidencia de un usuario'

    idIncidencia = fields.Integer(string="ID Incidencia", readonly=True)
    descripcion = fields.Char(required=True)

    usuario_id = fields.Many2one('simagrow.usuario', string="Usuario", required=True)

    @api.model
    def create(self, vals):
        usuario = self.env['simagrow.usuario'].browse(vals['usuario_id'])

        last_incidencia = self.search([('usuario_id', '=', usuario.id)], order='idIncidencia desc', limit=1)
        if last_incidencia:
            vals['idIncidencia'] = last_incidencia.idIncidencia + 1
        else:
            vals['idIncidencia'] = 1  

        record = super(Incidencia, self).create(vals)

        usuario.num_incidencias = len(usuario.incidencia_ids)

        return record
