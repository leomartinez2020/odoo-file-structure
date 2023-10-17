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
    inmueble_ids = fields.One2many("fincaraiz.inmueble", "inmueble_tipo_id", string="Inmuebles")

    # Computed (for stat button)
    conteo_ofertas = fields.Integer(string="Conteo de ofertas", compute="_compute_oferta")
    oferta_ids = fields.Many2many("fincaraiz.inmueble.oferta", string="Ofertas", compute="_compute_oferta")

    # ---------------------------------------- Compute methods ------------------------------------

    def _compute_oferta(self):
        # This solution is quite complex. It is likely that the trainee would have done a search in
        # a loop.
        data = self.env["fincaraiz.inmueble.oferta"].read_group(
            [("inmueble_id.estado", "!=", "cancelado"), ("inmueble_tipo_id", "!=", False)],
            ["ids:array_agg(id)", "inmueble_tipo_id"],
            ["inmueble_tipo_id"],
        )
        mapped_count = {d["inmueble_tipo_id"][0]: d["inmueble_tipo_id_conteo"] for d in data}
        mapped_ids = {d["inmueble_tipo_id"][0]: d["ids"] for d in data}
        for prop_type in self:
            prop_type.conteo_ofertas = mapped_count.get(prop_type.id, 0)
            prop_type.oferta_ids = mapped_ids.get(prop_type.id, [])
