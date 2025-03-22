from odoo import models,fields,api

class HmsDoctor(models.Model):
    _name = "hms.doctor"
    _description = "Doctor Information"

    first_name = fields.Char()
    last_name = fields.Char()
    image = fields.Binary()
    name = fields.Char( compute='_compute_name', store=True)


    
    #(ex1)
    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.first_name} {record.last_name}"

    # To show the name when creating a new model (ex2)
    # (name_get)is a function in odoo that is used to determine how the name will be displayed
    #def name_get(self):
       #result = []
       #for record in self:
         #result.append((record.id,f"{record.first_name} {record.last_name}"))
       #return result

