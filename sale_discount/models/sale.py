# -*- coding: utf-8 -*-

from openerp.osv import osv, fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp


class SaleOrderLine(osv.osv):
    _inherit = 'sale.order.line'

    def _get_subtotal_without_discount(self, cr, uid, ids, args, field_name, context=None):
        context = context or {}
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = (line.product_uom_qty * line.price_unit)
        return res

    def _get_discount(self, cr, uid, ids, args, field_name, context=None):
        context = context or {}
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.discount * line.subtotal_wo_discount / 100
        return res

    _columns = {
        'subtotal_wo_discount': fields.function(_get_subtotal_without_discount, string='SubTotal w/o Discount',
                                                store=True, type='float', digits_compute=dp.get_precision('Account')),
        'discount_amount': fields.function(_get_discount, string='Discount Amount',
                                           store=False, type='float', digits_compute=dp.get_precision('Account'),
                                           help='Amount total of the discount,\is calculated as Discount * \
                                           SubTotal w/o Discount / 100.'),
    }

class SaleOrder(osv.osv):

    _inherit = 'sale.order'

    def _amount_all_wrapper(self, cr, uid, ids, field_name, arg, context=None):
        """ Wrapper because of direct method passing as parameter for function fields """
        return self._get_function(cr, uid, ids, field_name, arg, context=context)

    def _get_function(self, cr, uid, ids, args, field_name, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
                'subtotal_wo_discount': 0.0,
                'discount_amount': 0.0,
            }
            amount = amount1 = val = val1 = 0.0
            cur = order.pricelist_id.currency_id
            for line in order.order_line:
                amount += line.subtotal_wo_discount
                amount1 += line.discount_amount
                val1 += line.price_subtotal
                val += self._amount_line_tax(cr, uid, line, context=context)
            res[order.id]['amount_tax'] = cur_obj.round(cr, uid, cur, val)
            res[order.id]['amount_untaxed'] = cur_obj.round(cr, uid, cur, val1)
            res[order.id]['amount_total'] = res[order.id]['amount_untaxed'] + res[order.id]['amount_tax']
            res[order.id]['subtotal_wo_discount'] = cur_obj.round(cr, uid, cur, amount)
            res[order.id]['discount_amount'] = cur_obj.round(cr, uid, cur, amount1)
        return res

    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('sale.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()

    _columns = {
        'amount_untaxed': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Untaxed Amount',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            },
            multi='sums', help="The amount without tax.", track_visibility='always'),
        'amount_tax': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Taxes',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            },
            multi='sums', help="The tax amount."),
        'amount_total': fields.function(_amount_all_wrapper, digits_compute=dp.get_precision('Account'), string='Total',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            },
            multi='sums', help="The total amount."),
        'subtotal_wo_discount': fields.function(_amount_all_wrapper,digits_compute=dp.get_precision('Account'), string= 'SubTotal wo Discount',
                                                store={'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                                                       'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
                                                        },
                                                multi='sums',help='Amount without apply the discount of the lines of the invoice.'),
        'discount_amount': fields.function(_amount_all_wrapper,digits_compute=dp.get_precision('Account'), string= 'SubTotal wo Discount',
                                                store={'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                                                       'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
                                                        },
                                                multi='sums',help='Total of discount apply in each line of the invoice.'),
    }
