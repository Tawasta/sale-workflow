
from odoo import fields, models


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    analytic_tag_name = fields.Char(related='analytic_tag_ids.name', store=True)
