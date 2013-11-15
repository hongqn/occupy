import os
import sys
import logging
import time
import types
from importlib import import_module
import weakref

from occupy.resource import Requirement

logger = logging.getLogger(__name__)


def populate_argparser(parser):
    parser.add_argument('module',
                        help="Module or package holding apply() function")


def main(args):
    start_time = time.time()

    sys.path.insert(0, os.getcwd())
    module = import_module(args.module)

    nfailed = apply_resource(module)

    time_cost = time.time() - start_time
    logging.info("Finished run in %.2f seconds", time_cost)

    if nfailed:
        logger.error("%d resources failed to apply", nfailed)

    return nfailed


def apply_resource(resource):
    applier = Applier()
    applier.apply(resource)
    return applier.nfailed


class Applier:
    def __init__(self):
        self.nfailed = 0
        self.applied = weakref.WeakSet()

    def apply(self, resource):
        nfailed = 0

        applied = (getattr(resource, 'applied', False) or
                   resource in self.applied)
        if applied:
            return nfailed

        try:
            resource.applied = True
        except AttributeError:
            self.applied.add(resource)

        if isinstance(resource, types.GeneratorType):
            for subresource in resource:
                failed = self.apply(subresource)
                if failed:
                    nfailed += failed
                    if isinstance(subresource, Requirement):
                        # requirement is not satisfied
                        break
            return nfailed

        try:
            if callable(resource):
                g = resource()
            else:
                logger.debug("Apply %s", resource)
                g = resource.apply()
        except Exception:
            logger.exception("Apply %s failed", resource)
            self.nfailed += 1
            return 1

        if isinstance(g, types.GeneratorType):
            return self.apply(g)
