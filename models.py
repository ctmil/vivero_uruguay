from odoo import fields, models, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    codigo_ncm = fields.Char('Codigo nomenclatura Mercosur')
