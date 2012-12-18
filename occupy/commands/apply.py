import logging
import time

def populate_argparser(parser):
    parser.add_argument('file')

def main(args):
    start_time = time.time()

    env = {}
    execfile(args.file, env)
    for resource in env['main']():
        resource()

    time_cost = time.time() - start_time
    logging.info("Finished run in %.2f seconds", time_cost)
