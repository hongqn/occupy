import logging
import abc
import types

logger = logging.getLogger(__name__)


class InvalidParameter(Exception):
    pass


class ResourceLogger(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        msg = "%s: %s" % (self.extra['resource'], msg)
        return msg, kwargs


class IDVAR:
    def __bool__(self):
        return False

    def __repr__(self):
        return "IDVAR"

IDVAR = IDVAR()


class ResourceMeta(abc.ABCMeta):
    def __new__(cls, name, bases, dict):
        dict['resources'] = {}
        return super().__new__(cls, name, bases, dict)

    def __getitem__(cls, id):
        return cls.resources[id]

    def __call__(cls, *args, **kwargs):
        resource = super().__call__(*args, **kwargs)
        cls.resources[resource.id] = resource
        return resource


class Resource(metaclass=ResourceMeta):
    def __init__(self, id, require=None):
        self.id = id.format_map(vars(self))
        self.require = require
        self.logger = ResourceLogger(logger, {'resource': self})

    def __str__(self):
        return "{self.__class__.__name__}[{self.id!r}]".format(self=self)

    def __call__(self):
        if self.require is not None:
            yield Requirement(self.require)

        self.logger.debug("Applying {}".format(self))
        retval = self.apply()
        if isinstance(retval, types.GeneratorType):
            yield from retval

    @abc.abstractmethod
    def apply(self):
        pass

    def s(self, tmpl):
        return tmpl.format_map(vars(self))



class Requirement:
    def __init__(self, require):
        self.require = require

    def __getattr__(self, name):
        return getattr(self.require, name)
