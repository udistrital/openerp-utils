#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import logging
import csv
from jinja2 import Environment, FileSystemLoader
from metamodel import Module
from cookiecutter.main import cookiecutter

from optparse import OptionParser

logging.basicConfig()
_logger = logging.getLogger('csv2model')

class dict_dot_access(dict):
    """Extension to make dict attributes be accesible with dot notation
    """
    __getattr__ = dict.__getitem__

def trim_vals(vals):
    for key, value in vals.items():
        if type(value) == str:
            vals[key] = value.strip()
    return vals

def main():
    usage = "Takes a CSV and creates a Odoo Module: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("-f", "--filename", dest="filename", help="CSV file")
    parser.add_option("-n", "--module_namespace", dest="module_namespace", help="Module namespace", default=False)
    parser.add_option("-m", "--module_name", dest="module_name", help="Module technical name", default='')
    parser.add_option("-s", "--module_string", dest="module_string", help="Module human name", default=False)
    parser.add_option("-g", "--generate", action="store_true", dest="generate_file", default=False, help="Generate CSV Template")
    parser.add_option("-d", "--debug", action="store_true", dest="debug", help="Display debug message", default=False)
    parser.add_option("-t", "--templates", dest="templates_dir", help="Templates folder",
        default=os.path.dirname(os.path.realpath(__file__)) + '/templates'
    )


    (options, args) = parser.parse_args()
    _logger.setLevel(0)
    if options.debug:
        _logger.setLevel(10)

    if options.generate_file:
        print """model_name,name,type,params,comodel,string,help,required,unique,constrains,onchange,view_tree,view_form,view_search,view_search_group_by,view_form_tab,menu,description,
print inherits,inherit,overwrite_write,overwrite_create
print petstore.pet,name,char,size:50,,Nombre,Nombre de la mascota,1,0,0,0,1,1,1,0,0,main,Pet,,mail.thread,,
print petstore.pet,state,selection,selection:Draft|Open|Closed;default:'draft',,Estado,Estados de la mascota,1,0,0,0,1,statusbar,1,1,0,,,,,,
print petstore.pet,user_id,many2one,readonly:True;default:_CURRENT_USER_,res.users,Usuario,Usuario asignado,0,0,0,0,1,_ATTRS_,"[('user_id','=',uid)]",1,0,,,,,,
print petstore.pet,age,float,compute:True;depends:birth_date,,Edad,Edad en Años,0,0,0,0,1,1,1,0,0,,,,,,
print petstore.pet,birth_date,date,default:_NOW_,,Fecha de nacimiento,Fecha de nacimiento,0,0,0,0,1,1,1,0,0,,,,,,
print petstore.pet,breed_id,many2one,,petstore.breed,Raza,Raza de la mascota,1,0,0,0,1,1,1,1,Raza,,,,,,
print petstore.pet,partner_id,many2one,"domain:[('is_company','=',False)]",res.partner,Dueño,Dueño de la mascota,1,0,0,0,1,1,1,1,Dueño,,,,,,
print petstore.breed,name,char,size:100,,Nombre,Nombre de la raza,1,1,0,0,1,1,1,0,0,conf,Raza de Mascotas,,,,
print petstore.breed,pet_ids,one2many,readonly:True,"petstore.pet,breed_id",Mascotas,Mascotas registradas para esta raza,0,0,0,0,0,1,0,0,0,,,,,,
print res.partner,pet_ids,one2many,,"petstore.pet,partner_id",Mascotas,Mascotas regitradas a este Partner,0,0,0,0,0,1,0,0,0,main,,,res.partner,,"""
        return

    if not options.filename:
        parser.error('CSV filename not given')

    env = Environment(loader=FileSystemLoader(options.templates_dir))

    module = Module(options.module_name, options.module_namespace, options.module_string)
    with open(options.filename, 'r') as handle:
        reader = csv.DictReader(handle)
        for line in reader:
            line = dict_dot_access(trim_vals(line))
            _logger.debug(line)
            model = module.add_model(line.model_name)
            model.description = line.description
            model.inherit = line.inherit
            model.inherits = line.inherits
            model.menu = line.menu
            model.overwrite_create = line.overwrite_create
            model.overwrite_write = line.overwrite_write
            field = model.add_field(line.name, line)

    output = {}
    for namespace in module.namespaces():
        output[namespace] = {}
        template = env.get_template("model_py.tpl")
        output[namespace]['py'] = template.render( {'module': module, 'namespace': namespace} )

        template = env.get_template("view_xml.tpl")
        output[namespace]['view'] = template.render( {'module': module, 'namespace': namespace} )

    for model in module.models:
        output[model.name] = {}
        template = env.get_template("test_py.tpl")
        output[model.name]['test'] = template.render( {'model': model} )
        template = env.get_template("data_csv.tpl")
        output[model.name]['data'] = template.render( {'model': model} )

    template = env.get_template("openerp_py.tpl")
    openerp_py = template.render( {'module': module} )

    template = env.get_template("test_init_py.tpl")
    test_init_py = template.render( {'module': module} )

    template = env.get_template("model_init_py.tpl")
    model_init_py = template.render( {'module': module} )

    template = env.get_template("acl_csv.tpl")
    acl_csv = template.render( {'module': module} )

    # Crear estructura del módulo en archivos
    cookiecutter(
        options.templates_dir + '/cookiecutter_template/',
        no_input=True,
        extra_context={
            'name': module.name,
            'namespace': module.namespace,
            'acl_csv': acl_csv,
            'model_py': output[module.namespace]['py'],
            'view_xml': output[module.namespace]['view'],
            'openerp_py': openerp_py,
            'test_init_py': test_init_py,
            'model_init_py': model_init_py,
        },
    )
    for namespace in module.namespaces():
        fname_py = '{0}/models/{1}.py'.format(module.name, namespace)
        fname_view = '{0}/views/{1}_view.xml'.format(module.name, namespace)
        with open(fname_py, "w") as f:
            f.write(output[namespace]['py'])
        with open(fname_view, "w") as f:
            f.write(output[namespace]['view'])

    for model in module.models:
        if model.namespace == module.namespace and model.menu == 'conf':
            fname_csv = '{0}/data/{1}.csv'.format(module.name, model.name)
            with open(fname_csv, "w") as f:
                f.write(output[model.name]['data'])
        elif model.namespace == module.namespace and model.menu != 'conf':
            fname_csv = '{0}/demo/{1}.csv'.format(module.name, model.name)
            with open(fname_csv, "w") as f:
                f.write(output[model.name]['data'])
            fname_test = '{0}/test/test_{1}.py'.format(module.name, model.name.replace('.', '_'))
            with open(fname_test, "w") as f:
                f.write(output[model.name]['test'])

if __name__ == '__main__':
    main()