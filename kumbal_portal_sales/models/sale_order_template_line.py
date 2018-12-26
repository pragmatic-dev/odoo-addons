# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError


class SaleOrderOption(models.Model):
    _inherit = 'sale.order.template.line'

    espiral = fields.Integer(string='Espiral', default=0)
    cantidad_maxima_por_espiral = fields.Integer(
        string='Cantidad Máxima Por Espiral',
        default=0
    )