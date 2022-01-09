# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Vinaya S B(<https://www.cybrosys.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import re
from odoo import api, fields, models


class PartnerEmailSMSHistory(models.Model):
    _inherit = 'res.partner'

    def action_view_partner_sms(self):
        self.ensure_one()
        action = self.env.ref('sms.sms_sms_action').read()[0]
        action['domain'] = [
            ('partner_id', '=', self.id)]
        return action

    def sent_email_history(self):
        action = self.env.ref('mail.action_view_mail_mail')
        result = action.read()[0]
        result['domain'] = [('email_from', '=', self.email)]
        return result

    def received_email_history(self):
        action = self.env.ref('mail.action_view_mail_mail')
        result = action.read()[0]
        result['domain'] = ['|', ('email_to', '=', self.email), ('recipient_ids', '=', self.email)]
        return result

    #    @api.depends('email')
    #    def get_email_valid(self):
    #        if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', self):
    #            return True
    #        else:
    #            return False

    email_valid = fields.Boolean(
        string='Email valid',
        default=lambda self: True if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', self.email) else False)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sms_history = fields.Boolean('SMS History', config_parameter='partner_emails_history.default_sms_history', default=False)
