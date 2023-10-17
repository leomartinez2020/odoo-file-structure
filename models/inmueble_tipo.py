# -*- coding: utf-8 -*-

from odoo import fields, models


class InmuebleTipo(models.Model):
# ---------------------------------------- Private Attributes ---------------------------------

    _name = "fincaraiz.inmueble.tipo"
    _description = "Tipo de Inmueble"

# --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    nombre = fields.Char("Nombre", required=True)

    # Relational (for inline view)
    property_ids = fields.One2many("fincaraiz.inmueble", "propiedad_tipo_id", string="Inmuebles")

