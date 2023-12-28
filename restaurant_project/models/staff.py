# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


class RestStaff(models.Model):
    _name = 'rest.staff'
    _description = 'This model will store the data of our staff.'
    _inherit = ['mail.thread','mail.activity.mixin']
    _rec_name = 'age'
    _order = 'age desc'


    name = fields.Char(string="Name", track_visibility="Always")
    age = fields.Integer(string="Age", track_visibility="Always", compute="_compute_age")
    dob = fields.Date(string="Birthdate")
    mobile = fields.Char(string="Mobile", track_visibility="Always")
    email = fields.Char(string="Email")
    country_id = fields.Many2one('res.country', string="Country")
    country_ids = fields.Many2many('res.country', string="Countries")
    department = fields.Many2one('rest.department', string="Department")
    country_code = fields.Char(string="Country Code", related="country_id.code")
    staff_line_ids = fields.One2many('rest.staff.lines', 'connecting_field', string="Staff Line")
    sequence = fields.Integer(string="Seq.")
    status = fields.Selection([('active', 'Active'), ('resign', 'Resigned')], string="Status", readonly=True, default="active", track_visibility="Always")
    gender = fields.Selection([('male','Male'), ('female','Female')], string = "Gender")
    image = fields.Binary(string="Iamge" )
    hand_salary = fields.Float(string="In Hand Salary")
    epf_esi = fields.Float(string="EPF+ESI")
    ctc_salary = fields.Float(string="CTC", compute="cal_ctc_salary")
    seq_no = fields.Char(string="Seq. No", index = True, readonly = True, copy = False, default = lambda self: _('New'))
    rating = fields.Selection([('0','very low'),('1','low'),('2','normal'),('3','high'),('4','very high'),('5','excellent')])
    active = fields.Boolean(string="Active", default=True)
    default_date = fields.Date(string="Date", default=lambda self:date.today())
    default_datetime = fields.Datetime(string="Datetime", default=lambda self:datetime.now())
    login_user = fields.Many2one('res.users', string="User", default=lambda self:self.env.user.id)
    user_company = fields.Many2one('res.company', string="Company", default=lambda self:self.env.user.company_id.id)
    button_integer = fields.Integer(string="Button Integer")
    mobile = fields.Char(string="Mobile")
    
    def share_on_whatsapp(self):
        if not self.mobile:
            raise ValidationError("missing mobile number in staff record.")
        message = 'Hi %s' % self.name
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.mobile, message)
        return{
        'type': 'ir.actions.act_url',
        'target': 'new',
        'url': whatsapp_api_url
        }

    def call_menu_fun(self):
        return
        
    def do_check_orm(self):
        return

    def unlink(self):
        for record in self:
            if record.status == 'active':
                raise UserError(_("we can't delete this record, record is in active mode."))
        return super(RestStaff, self).unlink()

    @api.model
    def create(self, vals):
        if vals.get("seq_no",_('New'))==_('New'):
            vals['seq_no'] = self.env['ir.sequence'].next_by_code('rest.seq.staff') or _('New')
        rec = super(RestStaff, self).create(vals)
        return rec

    def delete_one2many(self):
        for record in self:
            if record.staff_line_ids:
                record.staff_line_ids = [(5, 0, 0)]
                return{
                    'effect': {
                        'fadeout': 'slow',
                        'type': 'rainbow_man',
                        'message': 'Record has been deleted successfully'
                    }
                }

    def do_resign(self):
        for rec in self:
            rec.status = 'resign'

    @api.constrains('age')
    def val_age(self):
        for rec in self:
            if rec.age <=18:
                raise ValidationError(_("the age must greter than 18"))

    @api.depends('default_date','dob')
    def _compute_age(self):
        for rec in self:
            if rec.dob:
                rec.age = relativedelta(rec.default_date, rec.dob).years
            else:
                rec.age = 0

    @api.depends('hand_salary','epf_esi')
    def cal_ctc_salary(self):
        for rec in self:
            ctc = 0
            if rec.hand_salary:
                ctc = ctc + rec.hand_salary
            if rec.epf_esi:
                ctc = ctc + rec.epf_esi 
            rec.ctc_salary = ctc


    class RestStaffLine(models.Model):
        _name = 'rest.staff.lines'
        _description = "This wizard will show  the data of Products"

        connecting_field = fields.Many2one('rest.staff', string="Staff Id")
        name = fields.Char(string="Name", required=True)
        product_id = fields.Many2one("product.product", string="Product")
        sequence = fields.Integer(string="Seq.")
        qty = fields.Integer(string="Qty")
