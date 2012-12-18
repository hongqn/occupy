def populate_argparser(parser):
    parser.add_argument('file')

def main(args):
    env = {}
    execfile(args.file, env)
    for resource in env['main']():
        resource()
