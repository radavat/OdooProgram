from odoo import models, fields


class RestStaffwizard(models.TransientModel):
    _name='rest.staff.wizard'
    _description='This wizard will update the data of our staff.'

    name = fields.Char(string="Name")
    age = fields.Integer(string="Age")
    dob = fields.Date(string="DOB")
    mobile = fields.Char(string="Mobile")
    email = fields.Char(string="Email")
    country_id = fields.Many2one('res.country', string="Country")
    country_ids = fields.Many2many('res.country', string="Countries")
    country_code = fields.Char(string="Country Code", related="country_id.code")
    staff_line_ids = fields.One2many('rest.staff.wizard.lines', 'connecting_field', string="Staff Line")
    status = fields.Selection([('active', 'Active'), ('resign', 'Resigned')], string="Status", readonly=True, default="active")
    gender = fields.Selection([('male','Male'), ('female','Female')], string = "Gender")
    image = fields.Binary(string="Iamge" )
    hand_salary = fields.Float(string="In Hand Salary")
    epf_esi = fields.Float(string="EPF+ESI")
    ctc_salary = fields.Float(string="CTC")

    def update_info_fun(self):
        active_id = self._context.get('active_id')
        browse_id = self.env['rest.staff'].browse(active_id)
        
        country_list = []
        for rec in self.country_ids:
            country_list.append(rec.id)

        country_lists = []
        for record in self.staff_line_ids:
            country_lists.append((0,0,{
                'name':record.name,
                'product_id':record.product_id.id
                }))
        browse_id.staff_line_ids = [(5,0,0)]
        vals = {
                'name':self.name,
                'age':self.age,
                'mobile':self.mobile,
                'dob':self.dob,
                'email':self.email,
                'country_id':self.country_id.id,
                'country_ids':[(6,0,country_list)],
                'staff_line_ids':country_lists
        }
        browse_id.write(vals)
        # return{
        #     'type':'ir.actions.do.nothing'
        # }

class RestStaffwizardLine(models.TransientModel):
        _name = 'rest.staff.wizard.lines'
        _description = "This wizard will show  the data of Products"

        connecting_field = fields.Many2one('rest.staff.wizard', string="Staff Id")
        name = fields.Char(string="Name", required=True)
        product_id = fields.Many2one("product.product", string="Product")
        sequence = fields.Integer(string="Seq.")