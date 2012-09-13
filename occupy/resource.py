import pkgutil

class TypeMeta(type):
    def __init__(cls, name, bases, dict):
        for base in bases:
            if base.__name__ == 'Type':
                base.register(cls.name, cls)


class Type(object):
    __metaclass__ = TypeMeta

    name = None  # should be overrided in subclasses
    registry = {}

    @classmethod
    def get(cls, name):
        return cls.registry.get(name)

    @classmethod
    def register(cls, name, klass):
        if name in cls.registry:
            raise Exception("name %s already registered for %s" % (
                name, cls.registry[name]))
        cls.registry[name] = klass

    @classmethod
    def scan_package(cls, pkg):
        for importer, modname, ispkg in \
                pkgutil.walk_packages(pkg.__path__, pkg.__name__+'.'):
            __import__(modname)
