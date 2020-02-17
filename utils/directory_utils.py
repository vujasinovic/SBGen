import os
from os.path import join


def create_directory(name):
    from main import this_folder
    directory = join(this_folder, name)

    if not os.path.exists(directory):
        os.mkdir(directory)

    return directory
