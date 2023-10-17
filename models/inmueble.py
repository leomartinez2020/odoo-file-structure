# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api

class Inmueble(models.Model):
    _name = "fincaraiz.inmueble"
    _description = "Inmueble"

    def _default_date_availability(self):
        return fields.Date.context_today(self) + relativedelta(months=3)

    nombre = fields.Char("Nombre", required=True)
    descripcion = fields.Text("Descripción")
    codigopostal = fields.Char("Código Postal")
    precio_esperado = fields.Float("Precio esperado", required=True)
    precio_venta = fields.Float("Precio de venta", copy=False, readonly=True)
    fecha_disponible = fields.Date("Disponible desde", default=lambda self: self._default_date_availability(), copy=False)
    alcobas = fields.Integer("Alcobas", default=2)
    area_habitable = fields.Integer("Área habitable (m2)")
    fachadas = fields.Integer("Fachadas")
    garaje = fields.Boolean("Garaje")
    jardin = fields.Boolean("Jardín")
    area_jardin = fields.Integer("Área del jardín (m2)")
    area_total = fields.Integer(
        string="Área total",
        compute="_compute_area_total",
        help="Área total de jardín y zona habitable",
    )
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

    # Relational
    inmueble_tipo_id = fields.Many2one("fincaraiz.inmueble.tipo", string="Tipo de Inmueble")
    usuario_id = fields.Many2one("res.users", string="Vendedor", default=lambda self: self.env.user)
    comprador_id = fields.Many2one("res.partner", string="Comprador", readonly=True, copy=False)
    etiqueta_ids = fields.Many2many("fincaraiz.inmueble.etiqueta", string="Etiquetas")
    oferta_ids = fields.One2many("fincaraiz.inmueble.oferta", "inmueble_id", string="Ofertas")

    # computed
    @api.depends('area_habitable', 'area_jardin')
    def _compute_area_total(self):
        for record in self:
            record.area_total = record.area_habitable + record.area_jardin

    @api.onchange("jardin")
    def _onchange_jardin(self):
        if self.jardin:
            self.area_jardin = 10
            self.orientacion_jardin = "N"
        else:
            self.area_jardin = 0
            self.orientacion_jardin = False
