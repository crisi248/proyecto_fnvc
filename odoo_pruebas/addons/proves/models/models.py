# -*- coding: utf-8 -*-

from odoo import models, fields, api

"""
El nom del model mark ha de ser computat per indicar l’alumne i l’assignatura
Fer un nou camp computat a partir de l’any de naixement per treure l’edat. 
Treue la quantitat d’assignatures d’un alumne i d’un professor
Fer que la nota per defecte al crear una nota en un alumne siga un número aleatori
"""


class student(models.Model):
    #_name = 'proves.student'
    #_description = 'Estudiantes'
    _inherit = "res.partner"

    #name = fields.Char(required=True)
    year = fields.Integer()
    photo = fields.Image(max_width=200, max_height=200)
    classroom = fields.Many2one('proves.classroom', ondelete='set null')
    subject = fields.Many2many('proves.subject')
    floor = fields.Integer(related='classroom.floor')
    age = fields.Integer(compute="_get_age")

    @api.depends("year")
    def _get_age(self):
        for s in self:
            s.age = int(fields.Date.to_string(fields.Date.today()).split('-')[0]) - s.year


class teacher(models.Model):
    _name = 'proves.teacher'
    _description = 'Profesores'

    name = fields.Char(required=True)
    year = fields.Integer()
    subjects = fields.One2many('proves.subject', 'teacher')
    classroom = fields.Many2many('proves.classroom')
    tutorias = fields.Many2many(comodel_name='proves.classroom', # El model en el que es relaciona
                            relation='teacher_tutor_classroom', # (opcional) el nom del la taula en mig
                            column1='teacher_id', # (opcional) el nom en la taula en mig de la columna d'aquest model
                            column2='classroom_id')  # (opcional) el nom de la columna de l'altre model.

class mark(models.Model):
    _name = 'proves.mark'
    _description = 'notas'

    name = fields.Char(compute="_nombre_alumno_asignatura", readonly=True)
    mark = fields.Integer()
    student = fields.Many2one('res.partner')
    subject = fields.Many2one('proves.subject')

    @api.depends('student', 'subject')
    def _nombre_alumno_asignatura(self):
        for m in self:
            m.name = str(m.student.name) + " " + str(m.subject.name)


class subject(models.Model):
    _name = 'proves.subject'
    _description = 'Asignaturas'

    name = fields.Char(required=True)
    course = fields.Selection([('1', 'Primero'),('2', 'Segundo')])
    teacher = fields.Many2one('proves.teacher', ondelete='set null')
    marks = fields.One2many('proves.mark', 'subject')

class classroom(models.Model):
    _name = 'proves.classroom'
    _description = 'Clase'

    name = fields.Char(required=True)
    floor = fields.Integer()
    student_list = fields.One2many('res.partner', 'classroom')
    teacher = fields.Many2many('proves.teacher')
    tutores = fields.Many2many(comodel_name='proves.teacher', # El model en el que es relaciona
                            relation='teacher_tutor_classroom', # (opcional) el nom del la taula en mig
                            column1='classroom_id', # (opcional) el nom en la taula en mig de la columna d'aquest model
                            column2='teacher_id')  # (opcional) el nom de la columna de l'altre model.

 