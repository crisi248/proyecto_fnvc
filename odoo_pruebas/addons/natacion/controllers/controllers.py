# -*- coding: utf-8 -*-
from odoo import http
import json

class Natacion(http.Controller):

    @http.route('/natacion/championship', auth='none', type='http', methods=['GET'], csrf=False)
    def championship_info(self, name=None, **kw):
        if not name:
            return "Parámetro 'name' es requerido"

        print(name)
        
        championship = http.request.env['natacion.championship'].sudo().search([('name', '=', name)], limit=1)
        
        if not championship:
            return f"Campeonato '{name}' no encontrado"
            
        return championship.get_championship_json()


    @http.route('/natacion/pagarcuota', auth='public', type='http',cors="*", csrf=False)
    def apiGet(self, **args):
        print(args, http.request.httprequest.method)
        if (http.request.httprequest.method == "POST"):
            print(http.request.httprequest.data)
            data = json.loads(http.request.httprequest.data)
            record = http.request.env["res.partner"].sudo().search([("id", "=",data["id"])])
            print(record)
            record.pagar_cuota()

            return http.request.make_json_response(
                record.read(["name"]),
                headers=None,
                cookies=None,
                status=200)
                