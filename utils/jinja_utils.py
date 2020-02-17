import jinja2

from const import javatypes as javatypes
from const.simpletypes import *


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


def to_lowercase(st):
    return st[0].lower() + st[1:]


def setup_jinja_environment(source):
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(source),
        trim_blocks=True,
        lstrip_blocks=True)


def set_filters(jinja_environment):
    jinja_environment.filters['javatype'] = javatype
    jinja_environment.filters['to_pascalcase'] = to_pascalcase
    jinja_environment.filters['to_lowercase'] = to_lowercase
