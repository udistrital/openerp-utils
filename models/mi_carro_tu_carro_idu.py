# -*- coding: utf-8 -*-
##############################################################################
#
#    Grupo I+D+I
#    Subdirección Técnica de Recursos Tecnológicos
#    Instituto de Desarrollo Urbano - IDU - Bogotá - Colombia
#    Copyright (C) IDU (<http://www.idu.gov.co>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, exceptions
from openerp.exceptions import Warning, AccessError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

TIPO_TRANSPORTE = [
    ('carro', 'Carro'),
    ('moto', 'Moto'),
    ('taxi', 'Táxi'),
]

class mi_carro_tu_carro_oferta(models.Model):
    _name = 'mi_carro_tu_carro.oferta'
    _description = 'Mi carro tu carro Oferta'

    #Fields
    origen = fields.Char('Origen')  # minimo de ruta
    destino = fields.Char('Destino') # max de ruta
    hora_viaje = fields.Datetime('Hora inicio de viaje')
    tipo_transporte = fields.Selection(
        TIPO_TRANSPORTE,
        'Tipo de Trasporte',
        required=True,
    )
    vacantes = fields.Integer('Vacantes')
    costo = fields.Integer('Costo')
    comentario = fields.Text('Comentario')
    user_id = fields.Many2one(
        'res.users',
        'Usuario',
        default=lambda self: self._context.get('uid', False)
    )
    state = fields.Selection(
        [
           ('inactivo', 'Desactivar Oferna'),
           ('activo', 'Activar Oferna'),
        ],
        default="inactivo",
    )
    # Campo det tipo ruta
    

