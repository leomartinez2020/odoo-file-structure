# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class InmuebleOferta(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "fincaraiz.inmueble.oferta"
    _description = "Oferta de Inmueble"

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    precio = fields.Float("Precio", required=True)

    # Special
    estado = fields.Selection(
        selection=[
            ("aceptado", "Aceptado"),
            ("rechazado", "Rechazado"),
        ],
        string="Estatus",
        copy=False,
        default=False,
    )

    # Relational
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    inmueble_id = fields.Many2one("fincaraiz.inmueble", string="Inmueble", required=True)
    # For stat button:
    inmueble_tipo_id = fields.Many2one(
        "fincaraiz.inmueble.tipo", related="inmueble_id.inmueble_tipo_id", string="Tipo de Inmueble", store=True
    )
