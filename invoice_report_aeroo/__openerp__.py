## -*- coding: utf-8 -*-
#################################################################################
#
#    OpenERP, Open Source Management Solution
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################


{
    "name" : "Invoice Report Aeroo",
    "version" : "0.1",
    "author" : "Ahmed Mnasri",
    "website" : "http://www.tanitecsolution.com/",
    "category" : "Generic Modules/Others",
    "depends" : [
        "account",
        "product",
        "report_aeroo",
		"code_tva",
        "invoice_discount"
    ],
    "description" : """ Invoice report aeroo """,
    "data" : [
			"report/invoice_report_view.xml",
			"view/currency_to_text_view.xml",
            "view/invoice_view.xml",
            "view/product_view.xml",
            "data/product_data.xml",
			],
    "demo" : [],
    "active": False,
    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
