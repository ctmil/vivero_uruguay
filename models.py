from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime

class ResPartner(models.Model):
    _inherit = 'res.partner'

    pedido_ids = fields.One2many(comodel_name='vivero.pedido',inverse_name='partner_id',string='Pedidos')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    codigo_ncm = fields.Char('Codigo nomenclatura Mercosur')

class Plants(models.Model):
    _name = 'vivero.planta'

    def unlink(self):
        for rec in self:
            if rec.pedido_ids:
                raise ValidationError('No se puede borrar. Hay pedidos')
        return super(Plants, self).unlink()

    @api.depends('pedido_ids')
    def _compute_total_pedido(self):
        for rec in self:
            res = 0
            if rec.pedido_ids:
                for pedido in rec.pedido_ids:
                    res += pedido.amount_total
            rec.total_pedido = res

    name = fields.Char("Nombre")
    price = fields.Float()
    pedido_ids = fields.One2many(comodel_name='vivero.pedido',inverse_name='plant_id',string='Pedidos')
    total_pedido = fields.Float('Total pedido',compute=_compute_total_pedido,store=True)

class Pedido(models.Model):
    _name = 'vivero.pedido'

    def btn_confirm(self):
        self.ensure_one()
        sequence = self.env['ir.sequence'].next_by_code('PEDIDO-UY')
        self.name = sequence
        self.state = 'confirmed'

    @api.constrains('qty')
    def check_qty(self):
        if self.qty == 0:
            raise ValidationError('La cantidad debe ser mayor a 0')

    @api.onchange('qty')
    def onchange_qty(self):
        for rec in self:
            if rec.qty > 0:
                rec.amount_total = rec.qty * rec.price_unit

    def write(self, vals):
        vals['last_write_date'] = datetime.now()
        return super(Pedido, self).write(vals)

    plant_id = fields.Many2one("vivero.planta", required=True)
    partner_id = fields.Many2one("res.partner", required=True)
    qty = fields.Integer('Cantidad')
    price_unit = fields.Float('Precio Unitario',related='plant_id.price')
    amount_total = fields.Float('Precio Total')
    last_write_date = fields.Datetime('Fecha Ultima Modif')
    state = fields.Selection(selection=[('draft','Borrador'),('confirmed','Confirmado')],default='draft')
    name = fields.Char('Nombre',default='Borrador')
    image = fields.Binary('Imagen')
