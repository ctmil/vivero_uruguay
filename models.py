from odoo import fields, models, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    codigo_ncm = fields.Char('Codigo nomenclatura Mercosur')

class Plants(models.Model):
    _name = 'vivero.planta'

    name = fields.Char("Nombre")
    price = fields.Float()
    pedido_ids = fields.One2many(comodel_name='vivero.pedido',inverse_name='plant_id',string='Pedidos')

class Pedido(models.Model):
    _name = 'vivero.pedido'

    @api.onchange('qty')
    def onchange_qty(self):
        for rec in self:
            if rec.qty > 0:
                rec.amount_total = rec.qty * rec.price_unit

    plant_id = fields.Many2one("vivero.planta", required=True)
    partner_id = fields.Many2one("res.partner", required=True)
    qty = fields.Integer('Cantidad')
    price_unit = fields.Float('Precio Unitario',related='plant_id.price')
    amount_total = fields.Float('Precio Total')
