import sys
from argparse import ArgumentParser
import logging

from colorlog import ColoredFormatter


def main():
    parser = ArgumentParser()
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
            module = __import__(module_name, globals(), locals(),
                                ['populate_argparser', 'main'], level=1)
            module.populate_argparser(subparser)
            subparser.set_defaults(func=module.main)

    args = parser.parse_args()

    setup_logger()

    if not args.subparser_command:
        parser.print_help()
        return

    return args.func(args)


def setup_logger():
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)s: %(message)s")
    root = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root.addHandler(handler)
    root.setLevel(logging.INFO)
