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

    def __init__(self, name):
        self.name = name
        self.logger = ResourceLogger(logger, {'resource': self})

    def __str__(self):
        return "{self.__class__.__name__}[{self.name!r}]".format(self=self)

    @abc.abstractmethod
    def apply(self):
        pass
