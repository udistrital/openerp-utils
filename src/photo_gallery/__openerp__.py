# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

{
    "name" : "Photo gallery",
    "version" : "0.1",
    "author" : "STRT - IDU",
    "website" : "www.idu.gov.co",
    "category" : "photo",
    "description": """
        This module helps to store photos to be linked to a business model and stored as ir.attachment instead of binary field
    """,
    "depends" : [
                 'base',
                 ],
    "data" : [
        'security/ir.model.access.csv',
        'photo_gallery_view.xml',
    ],
    "installable": True
}