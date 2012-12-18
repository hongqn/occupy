import os

from occupy.resource import Resource, NAMEVAR, InvalidParameter

@Resource.register
class File(Resource):
    params = {
        'content': '',
        'path': NAMEVAR,
    }

    def __init__(self, name, **params):
        super(File, self).__init__(name, **params)
        if not self.path.startswith(os.sep):
            raise InvalidParameter("File paths must be fully qualified, not %r" % self.path)

    def __call__(self):
        if os.path.exists(self.path):
            current_content = open(self.path, 'rb').read()
        else:
            current_content = None

        if current_content != self.content:
            open(self.path, 'wb').write(self.content)
