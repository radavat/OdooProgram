# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class RestDepartment(models.Model):
    _name = 'rest.department'
    _description = 'This model will show the data of our department.'
    _rec_name='seq_no'

    @api.model
    def create(self, vals):
        if vals.get("seq_no",_('New'))==_('New'):
            vals['seq_no'] = self.env['ir.sequence'].next_by_code('rest.depart.seq') or _('New')
        rec = super(RestDepartment, self).create(vals)
        return rec

    sequence = fields.Integer(string="Seq.")
    seq_no = fields.Char(string="Seq. No", index = True, readonly = True, copy = False, default = lambda self: _('New'))
    name = fields.Char(string="Name")