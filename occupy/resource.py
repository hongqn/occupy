import pkgutil
import logging

logger = logging.getLogger(__name__)

class Resource(object):
    registry = {}

    def __init__(self, name):
        self.name = name
        self.logger = logging.LoggerAdapter(logger, {'resource': self})

    def __str__(self):
        return "{self.__class__.__name__}({self.name!r})".format(self=self)

    @classmethod
    def get(cls, name):
        return cls.registry.get(name)

    @classmethod
    def register(cls, name):
        def _(klass):
            if name in cls.registry:
                raise Exception("name %s already registered for %s" % (
                    name, cls.registry[name]))
            cls.registry[name] = klass
            return klass
        return _

    @classmethod
    def scan_package(cls, pkg):
        for importer, modname, ispkg in \
                pkgutil.walk_packages(pkg.__path__, pkg.__name__+'.'):
            __import__(modname)

    @classmethod
    def iter_all(cls):
        return []
