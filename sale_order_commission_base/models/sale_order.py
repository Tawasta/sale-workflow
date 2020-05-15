
from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    commission_base = fields.Float(
        string="Commission Base",
        compute="_compute_commission_base",
        search="_search_commission_base",
    )

    @api.multi
    def _search_commission_base(self, operator, value):
        recs = self.search([]).filtered(
            lambda x: x.commission_base)
        if recs:
            return [('id', 'in', [x.id for x in recs])]

    def _compute_commission_base(self):
        for record in self:
            lines = record.mapped('order_line')
            price = [(x.price_unit * x.product_uom_qty - x.discount) for x in lines]
            record.commission_base = sum(price)
