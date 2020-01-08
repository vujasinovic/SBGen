import os
from os.path import join, dirname

import jinja2
from textx import metamodel_from_file
from textx.export import metamodel_export, model_export

from const import javatypes as javatypes
from const.dot_export import *
from const.simpletypes import *

GENERATED_APP_DIRECTORY = 'generated_app'

this_folder = dirname(__file__)


class SimpleType(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def __str__(self):
        return self.name


def export_models(metamodel, model, dot_directory):
    metamodel_export(metamodel, join(dot_directory, META_MODEL_DOT))

    model_export(model, join(dot_directory, MODEL_DOT))


def get_entity_metamodel():
    simple_types = {
        BYTE: SimpleType(None, BYTE),
        SHORT: SimpleType(None, SHORT),
        INT: SimpleType(None, INT),
        LONG: SimpleType(None, LONG),
        FLOAT: SimpleType(None, FLOAT),
        DOUBLE: SimpleType(None, DOUBLE),
        BOOLEAN: SimpleType(None, BOOLEAN),
        CHAR: SimpleType(None, CHAR),
        STRING: SimpleType(None, STRING)
    }
    return metamodel_from_file('meta/entity.tx', classes=[SimpleType], builtins=simple_types)


def javatype(s):
    return {
        STRING: javatypes.STRING,
        CHAR: javatypes.CHAR,
        BOOLEAN: javatypes.BOOLEAN,
        DOUBLE: javatypes.DOUBLE,
        FLOAT: javatypes.FLOAT,
        LONG: javatypes.LONG,
        INT: javatypes.INT,
        SHORT: javatypes.SHORT,
        BYTE: javatypes.BYTE,
    }.get(s.name, s.name)


def to_pascalcase(st):
    return st[0].upper() + st[1:]


def create_directory(name):
    directory = join(this_folder, name)

    if not os.path.exists(directory):
        os.mkdir(directory)

    return directory


def setup_jinja_environment(source):
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(source),
        trim_blocks=True,
        lstrip_blocks=True)


def set_filters(jinja_environment):
    jinja_environment.filters['javatype'] = javatype
    jinja_environment.filters['to_pascalcase'] = to_pascalcase


def main():
    metamodel = get_entity_metamodel()

    dot_directory = create_directory(DIRECTORY_NAME)

    model_directory = create_directory(GENERATED_APP_DIRECTORY + "\\model")

    jinja_environment = setup_jinja_environment(this_folder)
    set_filters(jinja_environment)

    template = jinja_environment.get_template('template/bom.template')

    user_model = metamodel.model_from_file('model/model.ent')

    for entity in user_model.entities:
        with open(join(model_directory, "%s.java" % entity.name), 'w') as file:
            file.write(template.render(entity=entity))

    export_models(metamodel, user_model, dot_directory)


if __name__ == "__main__":
    main()
