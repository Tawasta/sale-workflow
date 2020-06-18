
from odoo import models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    def compute_global_discount(self):
        pricelist = self.pricelist_id
        sale_line_model = self.env['sale.order.line']
        categ_products = {}

        for line in self.order_line:
            product_category = line.product_id.categ_id
            if product_category:
                qty = categ_products.get(
                    product_category, [0, list(sale_line_model)]
                )
                categ_products[product_category] = [
                    qty[0] + line.product_uom_qty, qty[1] + [line]
                ]

        items = pricelist.mapped('item_ids')

        for categ in categ_products:
            for line in categ_products.get(categ)[1]:
                biggest_qty = max(items.mapped('min_quantity'))
                smallest_qty = 0
                index = 0
                item_price = 0
                while smallest_qty < biggest_qty:
                    if index == len(items):
                        break
                    item = items[index]

                    if (item.product_tmpl_id and item.product_tmpl_id.categ_id
                            == categ and item.min_quantity <=
                            categ_products.get(categ)[0] and
                            item.product_tmpl_id ==
                            line.product_id.product_tmpl_id):
                        smallest_qty = item.min_quantity
                        item_price = item.price_surcharge
                    index += 1
                if item_price:
                    line.price_unit = item_price
