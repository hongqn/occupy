import sys
from argparse import ArgumentParser
import logging

from colorlog import ColoredFormatter


def main():
    parser = ArgumentParser()
    _add_loglevel_argument(parser)
    subparsers = parser.add_subparsers(title="Available subcommands",
                                       dest='subparser_command')

    subcommands = [
        ('resource', 'resource',
         "API only: interact directly with resources via the RAL."),
        ('apply', 'apply',
         "Apply occupy manifests locally"),
    ]

    for command, module_name, help_text in subcommands:
        subparser = subparsers.add_parser(command, help=help_text)
        if command in sys.argv:
            _add_loglevel_argument(subparser)
            module = __import__(module_name, globals(), locals(),
                                ['populate_argparser', 'main'], level=1)
            module.populate_argparser(subparser)
            subparser.set_defaults(func=module.main)

    args = parser.parse_args()

    setup_logger(args.loglevel)

    if not args.subparser_command:
        parser.print_help()
        return

    return args.func(args)


def _add_loglevel_argument(parser):
    parser.add_argument(
        '-v', '--verbose', dest='loglevel', action='store_const',
        const=logging.DEBUG, default=logging.INFO,
        help="Show debug information")
    parser.add_argument(
        '-q', '--quiet', dest='loglevel', action='store_const',
        const=logging.WARNING, default=logging.INFO,
        help="Show less verbose information")


def setup_logger(loglevel):
    formatter = ColoredFormatter(
        "%(log_color)s%(message)s")
    root = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root.addHandler(handler)
    root.setLevel(loglevel)
