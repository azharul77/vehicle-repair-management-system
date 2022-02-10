from odoo import models, fields, _, api
from odoo.exceptions import ValidationError

class Services(models.Model):
    _name = 'vehicle.services'
    _description = "Services Table"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    service_name = fields.Char(string="Service Name", requird=True)
    service_charge = fields.Integer(string="Service Charge")
    service_product = fields.Many2one(
        string='Service Product',
        comodel_name='product.product')

    @api.onchange('service_product')
    def onchange_amount(self):
        for rec in self:
            if rec.service_product:
                rec.service_charge = rec.service_product.lst_price