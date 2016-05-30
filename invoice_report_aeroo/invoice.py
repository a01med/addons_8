# -*- coding: utf-8 -*- 

import itertools
from lxml import etree

from openerp import models, fields, api,_
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp.tools import float_compare
import openerp.addons.decimal_precision as dp


class account_invoice(models.Model):
    _inherit = ['account.invoice']
    _description = "Invoice"
    _order = "number desc, id desc"
    
    @api.one
    @api.depends('invoice_line.price_subtotal', 'tax_line.amount')
    def _compute_amount(self):
        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line)
        self.amount_tax = sum(line.amount for line in self.tax_line)
        self.amount_total = self.amount_untaxed + self.amount_tax
        self.ht = self.amount_untaxed - 0.5
        self.ht_wo_discount = sum((line.quantity * line.price_unit) for line in self.invoice_line) - 0.5

    ht = fields.Float(string='net', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_compute_amount')
    ht_wo_discount = fields.Float(string='ht', digits=dp.get_precision('Account'),
        store=True, readonly=True, compute='_compute_amount')

