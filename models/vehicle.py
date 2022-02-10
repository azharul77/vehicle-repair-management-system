from datetime import datetime
from odoo import models, fields, _, api
from odoo.exceptions import ValidationError

class VehicleInfo(models.Model):
    _name = 'vehicle.info'
    _description = 'vehicle record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # @api.onchange('vehicle_number')
    # def set_customer_status(self):
    #     is_exist = self.env['vehicle.info'].search([('vehicle_number','=',self.vehicle_number)])
    #     if is_exist:
    #         self.customer_type = 'old'
    #     else:
    #         self.customer_type = 'new'  

    @api.depends('vehicle_number')
    def set_customer_status(self):
        for rec in self:
            if rec.vehicle_number:
                if rec.vehicle_number == self.vehicle_number:
                    rec.customer_type = 'new'
                else:
                    rec.customer_type = 'old'

    vehicle_number =  fields.Char(string='Vehicle Number', required=True, track_visibility='always')
    vehicle_type = fields.Selection([
        ('2wheeler', '2 Wheeler'),
        ('3wheeler', '3 Wheeler'),
        ('4wheeler', '4 Wheeler'),
    ], default='2wheeler', String='Vehicle Type')
    vehicle_model =  fields.Char(string='Vehicle Model Number', required=True)
    vehicle_owner =  fields.Char(string='Owner Name ', required=True)
    customer_phone_number = fields.Integer(string='Customer Phone Number')
    service_date = fields.Date(string='Date Of Servoce', required=True)
    service_list = fields.Many2many(
        "vehicle.services", "vehicle_service_rel", "vehicle_id", "service_id", string="Services")
    service_product_ids = fields.Many2many(
        string='Service Product',
        comodel_name='product.product')
    service_amount_move_id = fields.Many2one(
        comodel_name="account.move", string="Invoice", track_visibility='onchange')    
    customer_type = fields.Selection(
        [('old', 'Old Customer'), ('new', 'New Customer'), ], string="Customer Type", compute="set_customer_status")
    notes = fields.Text(string='Maintain Customer Detail')


    @api.model
    def create(self, vals):
        
        res = super(VehicleInfo, self).create(vals)
        vals['code'] = self.env['ir.sequence'].next_by_code('vehicle.info')
        self.create_invoice_service(res)

        return res

    def create_invoice_service(self, record):
        if record:
            if not record.service_amount_move_id:

                invoice_line_ids = []
                for x in record.service_list:
                    invoice_line_ids.append([0, 0, {
                        'product_id': x.service_product.id,
                        'name': x.service_product.name,
                        'account_id': False,
                        'price_unit': x.service_product.list_price,
                        'quantity': 1.0,
                        'discount': 0.0,
                        'product_uom_id': x.service_product.uom_id.id,
                    }])
                account_move = self.env['account.move'].sudo().create({
                    'name': "INV/CLUB/" + str(datetime.now().year) + "/" + str(record.vehicle_number) + "/" + str(record.vehicle_owner),
                    'partner_id': record.id,
                    'ref': str(record.id),
                    'type': 'out_invoice',
                    'invoice_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'invoice_line_ids': invoice_line_ids,
                })
                if account_move:
                    invoice_post_status = account_move.sudo().action_post()
                    record.sudo().write({
                        'service_amount_move_id': account_move.id,
                    })   



