import os
from importlib import import_module


def read(module, *path):
    if isinstance(module, str):
        module = import_module(module)

    path = os.path.join(os.path.dirname(module.__file__), *path)
    with open(path, 'rb') as f:
        return f.read()
