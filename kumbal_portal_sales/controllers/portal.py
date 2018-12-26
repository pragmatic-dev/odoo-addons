# -*- coding: utf-8 -*-

from odoo import http
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.sale.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):

    @http.route(["/my/orders/<int:order_id>/add_all_options"], type='http', auth="public", website=True)
    def add_all_options(self, order_id, access_token=None, **post):
        try:
            order_sudo = self._document_check_access(
                'sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        order_sudo.add_all_options_to_order()

        return request.redirect(order_sudo.get_portal_url(anchor='details'))
