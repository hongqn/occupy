import os
from importlib import import_module

from mako.template import Template

from occupy.facter import facts

__all__ = ['read', 'render']


def read(module, *path):
    path = _resolve_module_relative_path(module, *path)
    with open(path, 'rb') as f:
        return f.read()


def render(module, *path):
    path = _resolve_module_relative_path(module, *path)
    template = Template(filename=path, strict_undefined=True)
    return template.render(facts=facts)


def _resolve_module_relative_path(module, *path):
    if isinstance(module, str):
        module = import_module(module)

    return os.path.join(os.path.dirname(module.__file__), *path)
