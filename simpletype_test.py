import os
from os.path import join, dirname

from textx import metamodel_from_file
from textx.export import metamodel_export, model_export

from const.dot_export import *
from const.simpletypes import *

this_folder = dirname(__file__)


class SimpleType(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name


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
    metamodel = metamodel_from_file('meta/entity.tx', classes=[SimpleType], builtins=simple_types)

    return metamodel


def main():
    metamodel = get_entity_metamodel()

    dot_directory = join(this_folder, DIRECTORY_NAME)

    if not os.path.exists(dot_directory):
        os.mkdir(dot_directory)

    metamodel_export(metamodel, join(dot_directory, META_MODEL_DOT))

    user_model = metamodel.model_from_file('model/user.ent')

    model_export(user_model, join(dot_directory, MODEL_DOT))


if __name__ == "__main__":
    main()
