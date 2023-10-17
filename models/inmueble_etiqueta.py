# -*- coding: utf-8 -*-

from odoo import fields, models


class InmuebleEtiqueta(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------

    _name = "fincaraiz.inmueble.etiqueta"
    _description = "Etiqueta del Inmueble"

    # --------------------------------------- Fields Declaration ----------------------------------

    # Basic
    nombre = fields.Char("Nombre", required=True)
    color = fields.Integer("Índice de Color")
