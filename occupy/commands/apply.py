import os
import sys
import logging
import time
import types
from collections import Iterable
from importlib import import_module

logger = logging.getLogger(__name__)


def populate_argparser(parser):
    parser.add_argument('module')


def main(args):
    start_time = time.time()

    sys.path.insert(0, os.getcwd())
    module = import_module(args.module)

    failed = apply_resource(module)

    time_cost = time.time() - start_time
    logging.info("Finished run in %.2f seconds", time_cost)

    if failed:
        logger.error("%d resources failed to apply", failed)

    return failed


def apply_resource(resource):
    if isinstance(resource, types.ModuleType):
        try:
            main = resource.main
        except AttributeError:
            logger.error("module %s has no main function",
                         resource.__name__)
            return 1

        if not callable(main):
            logger.error("%s.main is not callable", resource.__name__)
            return 1

        return apply_resource(main())

    elif isinstance(resource, Iterable):
        failed = 0
        for subresource in resource:
            failed += apply_resource(subresource)
        return failed

    else:
        logger.info("Applying %s", resource)
        try:
            resource()
        except Exception:
            logger.exception("Apply %s failed", resource)
            return 1
        else:
            return 0
