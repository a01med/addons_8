# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import math
import re
import time
from openerp import api, tools, SUPERUSER_ID
from openerp.osv import osv, fields, expression
from openerp.tools.translate import _


class product_template(osv.osv):
    _name = 'product.template'
    _inherit = 'product.template'

    _columns = {
#            'type': fields.selection([('product', 'Stockable Product'),('consu', 'Consumable'),('service','Service'),('stamp','Tembre')], 'Product Type', required=True, help="Consumable are product where you don't manage stock, a service is a non-material product provided by a company or an individual."),        
            'stamp': fields.boolean('T.F'),
    }

    _defaults = {
 #       'type' : 'consu',
        'stamp': True
    }
    