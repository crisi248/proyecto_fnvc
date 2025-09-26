# -*- coding: utf-8 -*-

from odoo import models, fields, api


class student(models.Model):
    _name = 'proves.student'
    _description = 'Estudiantes'

    name = fields.Char(required=True)
    year = fields.Integer()
    photo = fields.Image(max_width=200, max_height=200)
    classroom = fields.Many2one('proves.classroom', ondelete='set null')
    subject = fields.Many2many('proves.subject')
    floor = fields.Integer(related='classroom.floor')


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

    name = fields.Char()
    mark = fields.Integer()
    student = fields.Many2one('proves.student')
    subject = fields.Many2one('proves.subject')

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
    student_list = fields.One2many('proves.student', 'classroom')
    teacher = fields.Many2many('proves.teacher')
    tutores = fields.Many2many(comodel_name='proves.teacher', # El model en el que es relaciona
                            relation='teacher_tutor_classroom', # (opcional) el nom del la taula en mig
                            column1='classroom_id', # (opcional) el nom en la taula en mig de la columna d'aquest model
                            column2='teacher_id')  # (opcional) el nom de la columna de l'altre model.

 