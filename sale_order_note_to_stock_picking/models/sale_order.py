from odoo import api, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        for pick in self.picking_ids:
            pick.write({"comment": self.note or ""})

        return res
