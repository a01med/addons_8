# -*- coding: utf-8 -*-
##############################################################################
#
# module for OpenERP,
# Copyright (C)   (<http://>)
#
# This file is a part of
#
#  is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    $1 is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class InvoiceGlobalDiscountWizard(models.TransientModel):
    _name = "invoice.global_discount.wizard"

    # todo implement fixed amount
    # type = fields.Selection([
    #     ('percentage', 'Percentage'),
    #     ('fixed_amount', 'Fixed Amount'),
    #     ],
    #     'Type',
    #     required=True,
    #     default='percentage',
    #     )
    amount = fields.Float(
        # 'Amount',
        'Discount',
        required=True,
        )

    @api.multi
    def confirm(self):
        self.ensure_one()
        invoice = self.env['account.invoice'].browse(
            self._context.get('active_id', False))
        for line in invoice.invoice_line:
            line.discount = self.amount
        return True

