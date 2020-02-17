from os.path import join, dirname

from textx import metamodel_from_file
from textx.export import metamodel_export, model_export

from const.dot_export import DIRECTORY_NAME, META_MODEL_DOT, MODEL_DOT
from utils.directory_utils import create_directory
from utils.jinja_utils import *

GENERATED_APP_DIRECTORY = 'C:\\JSD\\generated_app\\src\\main\\java'

this_folder = dirname(__file__)


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


def export_models(metamodel, model, dot_directory):
    metamodel_export(metamodel, join(dot_directory, META_MODEL_DOT))

    model_export(model, join(dot_directory, MODEL_DOT))


class SimpleType(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name

    def __str__(self):
        return self.name


def main():
    metamodel = get_entity_metamodel()
    dot_directory = create_directory(DIRECTORY_NAME)

    main_class_directory = create_directory(GENERATED_APP_DIRECTORY)
    model_directory = create_directory(GENERATED_APP_DIRECTORY + "\\model")
    repository_directory = create_directory(GENERATED_APP_DIRECTORY + "\\repository")
    service_directory = create_directory(GENERATED_APP_DIRECTORY + "\\service")
    service_impl_directory = create_directory(GENERATED_APP_DIRECTORY + "\\service\\implementation")
    controller_directory = create_directory(GENERATED_APP_DIRECTORY + "\\controller")

    jinja_environment = setup_jinja_environment(this_folder)
    set_filters(jinja_environment)

    main_class_template = jinja_environment.get_template('template/main_class.template')
    bom_template = jinja_environment.get_template('template/bom.template')
    repository_template = jinja_environment.get_template('template/repository.template')
    service_template = jinja_environment.get_template('template/service.template')
    service_impl_template = jinja_environment.get_template('template/service_impl.template')
    controller_template = jinja_environment.get_template('template/controller.template')

    user_model = metamodel.model_from_file('model/model.ent')

    for entity in user_model.entities:
        with open(join(main_class_directory, "Application.java"), 'w') as file:
            file.write(main_class_template.render())
        with open(join(model_directory, "%s.java" % entity.name), 'w') as file:
            file.write(bom_template.render(entity=entity))
        with open(join(repository_directory, "%sRepository.java" % entity.name), 'w') as file:
            file.write(repository_template.render(entity=entity))
        with open(join(service_directory, "%sService.java" % entity.name), 'w') as file:
            file.write(service_template.render(entity=entity))
        with open(join(service_impl_directory, "%sServiceImpl.java" % entity.name), 'w') as file:
            file.write(service_impl_template.render(entity=entity))
        with open(join(controller_directory, "%sController.java" % entity.name), 'w') as file:
            file.write(controller_template.render(entity=entity))

    export_models(metamodel, user_model, dot_directory)


if __name__ == "__main__":
    main()
