# -*- coding: utf-8 -*-

from odoo import models, fields, api

class productos(models.Model):

    _inherit = 'product.template'

    is_destacado = fields.Boolean()
    texto_publicitario = fields.Char(required=True)


class destacar_productos_wizard(models.TransientModel):
    _name = 'productos.destacar_productos'

    is_destacado_wizard = fields.Boolean()
    texto_publicitario_wizard = fields.Char()

    state = fields.Selection([
        ('seleccionar', "Seleccionar Productos"),
        ('destacar', "Destacar Productos")                                                                     
      ], default='seleccionar')

    def _default_productos(self):
         return self.env['product.template'].browse(self.env.context.get('active_ids'))

    productos_id = fields.Many2many(
        "product.template",
        default = _default_productos
    )

    def destacar_producto(self):

        for producto in self.productos_id:
            producto.write({'is_destacado':self.is_destacado_wizard, 'texto_publicitario':self.texto_publicitario_wizard})

        return {"type": "ir.actions.client", "tag": "reload"}
    
    def next(self):

        self.state = 'destacar'

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def previous(self):
        self.state = 'seleccionar'

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
    
    



    