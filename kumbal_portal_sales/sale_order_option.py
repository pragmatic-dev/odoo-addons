# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError


class SaleOrderOption(models.Model):
    _inherit = 'sale.order.option'

    espiral = fields.Integer(string='Espiral', default=0)
    cantidad_maxima_por_espiral = fields.Integer(
        string='Cantidad Máxima Por Espiral',
        default=0
    )

    @api.multi
    def _get_values_to_add_to_order(self):
        values = super(SaleOrderOption, self)._get_values_to_add_to_order()
        values['espiral'] = self.espiral
        values['cantidad_maxima_por_espiral'] = self.cantidad_maxima_por_espiral
        return values
