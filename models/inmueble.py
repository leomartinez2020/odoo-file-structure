# -*- coding: utf-8 -*-

from odoo import fields, models, api

class Inmueble(models.Model):
    _name = "fincaraiz.inmueble"
    _description = "Inmueble"

    nombre = fields.Char("Nombre", required=True)
    descripcion = fields.Text("Descripción")
    codigopostal = fields.Char("Código Postal")
    precio_esperado = fields.Float("Precio esperado", required=True)
    precio_venta = fields.Float("Precio de venta", copy=False, readonly=True)
    fecha_disponible = fields.Date("Disponible desde", default=lambda self: fields.Datetime.now(), copy=False)
    alcobas = fields.Integer("Alcobas", default=2)
    area_habitable = fields.Integer("Área habitable (m2)")
    fachadas = fields.Integer("Fachadas")
    garaje = fields.Boolean("Garaje")
    jardin = fields.Boolean("Jardín")
    area_jardin = fields.Integer("Área del jardín (m2)")
    area_total = fields.Integer(string="Área total", compute="_compute_area_total")
    activo = fields.Boolean("Activo", default=True)
    orientacion_jardin = fields.Selection(
        selection=[
            ("N", "Norte"),
            ("S", "Sur"),
            ("E", "Este"),
            ("O", "Oeste"),
        ],
        string="Orientacion del jardín",
    )

    # Relational
    propiedad_tipo_id = fields.Many2one("fincaraiz.inmueble.tipo", string="Tipo de Inmueble")
    usuario_id = fields.Many2one("res.users", string="Vendedor", default=lambda self: self.env.user)
    comprador_id = fields.Many2one("res.partner", string="Comprador", readonly=True, copy=False)

    estado = fields.Selection(
        selection=[
            ("nuevo", "Nuevo"),
            ("oferta_recibida", "Oferta Recibida"),
            ("oferta_aceptada", "Oferta Aceptada"),
            ("vendido", "Vendido"),
            ("cancelado", "Cancelado"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="nuevo",
    )

    @api.depends('area_habitable', 'area_jardin')
    def _compute_area_total(self):
        for record in self:
            record.area_total = record.area_habitable + record.area_jardin

    @api.onchange("jardin")
    def _onchange_garden(self):
        if self.jardin:
            self.jardin_area = 10
            self.orientacion_jardin = "N"
        else:
            self.area_jardin = 0
            self.orientacion_jardin = False
