from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    total_delivery_weight = fields.Float(compute="_compute_pricelist_weight")
    max_weight = fields.Float(related="carrier_id.max_weight")

    @api.depends('order_line.product_uom_qty', 'order_line.product_id')
    def _compute_pricelist_weight(self):
        for sale in self:
            sale.total_delivery_weight = sum(
                    [x.product_id.weight * x.product_uom_qty for x in sale.order_line])
            if sale.carrier_id.max_weight < sale.total_delivery_weight:
                sale.carrier_id = None
