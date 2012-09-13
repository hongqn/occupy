import argparse
import textwrap

from occupy.resource import Type
import occupy.types

def populate_argparser(parser):
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.description = textwrap.dedent(
        """\
        This command provides simple facilities for converting current system
        state into Occupy code, along with some ability to modify the current
        state using Occupy's RAL.

        By default, you must at least provide a type to list, in which case
        occupy resource will tell you everything it knows about all resources
        of that type. You can optionally specify an instance name, and occupy
        resource will only describe that single instance.

        If given a type, a name, and a series of <attribute>=<value> pairs,
        occupy resource will modify the state of the specified resource.
        """)
    parser.add_argument('type')

def main(args):
    Type.scan_package(occupy.types)
    type = Type.get(args.type)
    if type is None:
        return "Could not find type %s" % args.type

