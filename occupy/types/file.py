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
        exists = os.path.exists(self.path)
        content = open(self.path, 'rb').read() if exists else None

        if content != self.content:
            open(self.path, 'wb').write(self.content)
            self.logger.info("updated" if exists else "created")
