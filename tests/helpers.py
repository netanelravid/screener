from os import path

ROOT = path.dirname(path.abspath(__file__))
RESOURCES_FOLDER = path.join(ROOT, 'resources')


def get_resource(filename):
    with open(path.join(RESOURCES_FOLDER, filename), 'r') as fp:
        return fp.read()
