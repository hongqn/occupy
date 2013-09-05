import logging
import time
from collections import Iterable

def populate_argparser(parser):
    parser.add_argument('file')

def main(args):
    start_time = time.time()

    env = {}
    exec(open(args.file).read(), env)

    def apply_resource(resource):
        if isinstance(resource, Iterable):
            for subresource in resource:
                apply_resource(subresource)
        else:
            resource()

    apply_resource(env['main']())

    time_cost = time.time() - start_time
    logging.info("Finished run in %.2f seconds", time_cost)
