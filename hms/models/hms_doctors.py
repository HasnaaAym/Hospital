from odoo import models,fields,api

class HmsDoctor(models.Model):
    _name = "hms.doctor"
    _description = "Doctor Information"

    FirstName = fields.Char()
    LastName = fields.Char()
    image = fields.Binary()
    name = fields.Char( compute='_compute_name', store=True)


    
    #(ex1)
    @api.depends('FirstName', 'LastName')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.FirstName} {record.LastName}"

    # To show the name when creating a new model (ex2)
    # (name_get)is a function in odoo that is used to determine how the name will be displayed
    #def name_get(self):
       #result = []
       #for record in self:
         #result.append((record.id,f"{record.FirstName} {record.LastName}"))
       #return result

