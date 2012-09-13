from occupy import File, template

def add_keywords(file, tmpl=None):
    if tmpl is None:
        tmpl = "{caller_module_name}/portage/package.keywords/{file}.mako"

    yield File('/etc/portage/package.keywords/{file}',
               content = template(tmpl))
