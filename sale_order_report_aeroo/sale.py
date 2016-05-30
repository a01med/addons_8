# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

class SaleOrder(osv.osv):
    _inherit = 'sale.order'

    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
    	cur_obj = self.pool.get('res.currency')
    	res = super(SaleOrder, self)._amount_all(cr, uid, ids, field_name, arg, context)
    	for order in self.browse(cr, uid, ids, context=context):
    		res [order.id] = { }
    		val1 = val2 = 0.0
    		for line in order.order_line:
    			val1 += line.price_subtotal
    			val2 += (line.product_uom_qty * line.price_unit)
    		res[order.id]['ht'] = val1 - 0.5
    		res[order.id]['ht_wo_discount'] = val2 - 0.5
    	return res

    _columns = {
            'ht': fields.function(_amount_all, method=True, digits_compute=dp.get_precision('Account'), string='Total',
                                            store=True, multi='sums', help="The total amount."),
			'ht_wo_discount': fields.function(_amount_all, method=True, digits_compute=dp.get_precision('Account'), string='Total',
                                            store=True, multi='sums', help="The total amount."),
            }