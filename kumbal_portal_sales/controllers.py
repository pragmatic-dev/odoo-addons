# -*- coding: utf-8 -*-
from odoo import http

# class KumbalPortalSales(http.Controller):
#     @http.route('/kumbal_portal_sales/kumbal_portal_sales/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kumbal_portal_sales/kumbal_portal_sales/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('kumbal_portal_sales.listing', {
#             'root': '/kumbal_portal_sales/kumbal_portal_sales',
#             'objects': http.request.env['kumbal_portal_sales.kumbal_portal_sales'].search([]),
#         })

#     @http.route('/kumbal_portal_sales/kumbal_portal_sales/objects/<model("kumbal_portal_sales.kumbal_portal_sales"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kumbal_portal_sales.object', {
#             'object': obj
#         })