import os
import sys
import logging
import time
import types
from collections import Iterable
from importlib import import_module

logger = logging.getLogger(__name__)


def populate_argparser(parser):
    parser.add_argument('module',
                        help="Module or package holding apply() function")


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
            apply = resource.apply
        except AttributeError:
            logger.error("module %s has no apply function",
                         resource.__name__)
            return 1

        if not callable(main):
            logger.error("%s.apply is not callable", resource.__name__)
            return 1

        return apply_resource(apply())

    elif isinstance(resource, Iterable):
        failed = 0
        for subresource in resource:
            failed += apply_resource(subresource)
        return failed

    else:
        try:
            resource.apply()
        except Exception:
            logger.exception("Apply %s failed", resource)
            return 1
        else:
            return 0
