import pkgutil
import logging
import abc

logger = logging.getLogger(__name__)


class InvalidParameter(Exception):
    pass


class ResourceLogger(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        msg = "%s: %s" % (self.extra['resource'], msg)
        return msg, kwargs


class NAMEVAR:
    def __bool__(self):
        return False

    def __repr__(self):
        return "NAMEVAR"

NAMEVAR = NAMEVAR()


class Resource:
    __metaclass__ = abc.ABCMeta

    registry = {}

    def __init__(self, name):
        self.name = name
        self.logger = ResourceLogger(logger, {'resource': self})

    def __str__(self):
        return "{self.__class__.__name__}[{self.name!r}]".format(self=self)

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

    @abc.abstractmethod
    def apply(self):
        pass


def scan_package(pkg):
    for importer, modname, ispkg in \
            pkgutil.walk_packages(pkg.__path__, pkg.__name__+'.'):
        __import__(modname)
