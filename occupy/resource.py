import pkgutil
import logging

NAMEVAR = object()

logger = logging.getLogger(__name__)

class InvalidParameter(Exception):
    pass

class ResourceLogger(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        msg = "%s: %s" % (self.extra['resource'], msg)
        return msg, kwargs

class Resource(object):
    registry = {}

    def __init__(self, name, **params):
        self.name = name
        self.logger = ResourceLogger(logger, {'resource': self})
        for para, default in self.params.items():
            if default is NAMEVAR and para not in params:
                setattr(self, para, name)
            else:
                setattr(self, para, params.get(para, default))

    def __str__(self):
        return "{self.__class__.__name__}({self.name!r})".format(self=self)

    @classmethod
    def get(cls, name):
        return cls.registry.get(name)

    @classmethod
    def register(cls, klass):
        name = klass.__name__
        if name in cls.registry:
            raise Exception("name %s already registered for %s" % (
                name, cls.registry[name]))
        cls.registry[name] = klass
        return klass

    @classmethod
    def iter_all(cls):
        return []


def scan_package(pkg):
    for importer, modname, ispkg in \
            pkgutil.walk_packages(pkg.__path__, pkg.__name__+'.'):
        __import__(modname)


