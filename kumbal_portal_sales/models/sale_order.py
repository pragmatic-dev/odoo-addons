# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _get_values_to_add_to_order_with_option(self, option):
        return {
            'order_id': self.id,
            'price_unit': option.price_unit,
            'name': option.name,
            'product_id': option.product_id.id,
            'product_uom_qty': option.quantity,
            'product_uom': option.uom_id.id,
            'discount': option.discount,
            'espiral': option.espiral,
            'cantidad_maxima_por_espiral': option.cantidad_maxima_por_espiral
        }

    @api.multi
    def add_all_options_to_order(self):
        self.ensure_one()
        order = self

        if order.state not in ['draft', 'sent']:
            raise UserError(_('You cannot add options to a confirmed order.'))

        for option in order.sale_order_option_ids:

            order_line = self.env['sale.order.line'].search([
                ('order_id', '=', self.id),
                ('product_id', '=', option.product_id.id)
            ], limit=1)

            if not order_line:
                values = self._get_values_to_add_to_order_with_option(option)

                order_line = self.env['sale.order.line'].create(values)
                order_line._compute_tax_id()

                option.write({'line_id': order_line.id})

    def unprocessed_option_lines(self):
        count = 0

        for option_line in self.sale_order_option_ids:
            if not option_line.line_id:
                count += 1

        return count

    def _compute_option_data_for_template_change(self, option):
        if self.pricelist_id:
            price = self.pricelist_id.with_context(
                uom=option.uom_id.id).get_product_price(option.product_id, 1, False)
        else:
            price = option.price_unit
        return {
            'product_id': option.product_id.id,
            'name': option.name,
            'quantity': option.quantity,
            'uom_id': option.uom_id.id,
            'price_unit': price,
            'discount': option.discount,
            'espiral': option.espiral,
            'cantidad_maxima_por_espiral': option.cantidad_maxima_por_espiral
        }

    @api.onchange('sale_order_template_id')
    def onchange_sale_order_template_id(self):
        if not self.sale_order_template_id:
            self.require_signature = self._get_default_require_signature()
            self.require_payment = self._get_default_require_payment()
            return
        template = self.sale_order_template_id.with_context(
            lang=self.partner_id.lang)

        order_lines = [(5, 0, 0)]
        for line in template.sale_order_template_line_ids:
            data = self._compute_line_data_for_template_change(line)
            if line.product_id:
                discount = 0
                if self.pricelist_id:
                    price = self.pricelist_id.with_context(
                        uom=line.product_uom_id.id).get_product_price(line.product_id, 1, False)
                    if self.pricelist_id.discount_policy == 'without_discount' and line.price_unit:
                        discount = (line.price_unit - price) / \
                            line.price_unit * 100
                        price = line.price_unit

                else:
                    price = line.price_unit

                data.update({
                    'price_unit': price,
                    'discount': 100 - ((100 - discount) * (100 - line.discount) / 100),
                    'product_uom_qty': line.product_uom_qty,
                    'product_id': line.product_id.id,
                    'product_uom': line.product_uom_id.id,
                    'customer_lead': self._get_customer_lead(line.product_id.product_tmpl_id),
                    'espiral': line.espiral,
                    'cantidad_maxima_por_espiral': line.cantidad_maxima_por_espiral,
                })
                if self.pricelist_id:
                    data.update(self.env['sale.order.line']._get_purchase_price(
                        self.pricelist_id, line.product_id, line.product_uom_id, fields.Date.context_today(self)))
            order_lines.append((0, 0, data))

        self.order_line = order_lines
        self.order_line._compute_tax_id()

        option_lines = []
        for option in template.sale_order_template_option_ids:
            data = self._compute_option_data_for_template_change(option)
            option_lines.append((0, 0, data))
        self.sale_order_option_ids = option_lines

        if template.number_of_days > 0:
            self.validity_date = fields.Date.to_string(
                datetime.now() + timedelta(template.number_of_days))

        self.require_signature = template.require_signature
        self.require_payment = template.require_payment

        if template.note:
            self.note = template.note
