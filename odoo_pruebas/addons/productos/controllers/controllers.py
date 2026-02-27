# -*- coding: utf-8 -*-
from odoo import http


class ProductosDescription(http.Controller):

    @http.route('/productos/description', auth='public')
    def list(self):
           record = http.request.env['product.template'].sudo().search([])
           return http.request.make_json_response(
               record.read(["name","texto_publicitario", "list_price", "is_destacado"]), 
               headers=None, 
               cookies=None, 
               status=200)

     


