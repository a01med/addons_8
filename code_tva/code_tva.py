from openerp.osv import fields, osv
from openerp.tools.translate import _

class res_partner(osv.osv):
    _inherit = 'res.partner' 
    #Do not touch _name it must be same as _inherit
    #_name = 'res.partner' 
    _columns = {
            'code_tva':fields.char('Code TVA', size=64),
			}
res_partner()