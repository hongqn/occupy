from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(title="Available subcommands",
                                       dest='subparser_command')

    subcommands = [
        ('resource', 'resource',
         "API only: interact directly with resources via the RAL."),
    ]

    for command, module_name, help_text in subcommands:
        module = __import__(module_name, globals(), locals(),
                            ['populate_argparser', 'main'], level=1)
        subparser = subparsers.add_parser(command, help=help_text)
        module.populate_argparser(subparser)
        subparser.set_defaults(func=module.main)

    args = parser.parse_args()
    return args.func(args)
