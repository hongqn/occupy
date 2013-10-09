import os
import difflib

from occupy.resource import Resource, NAMEVAR, InvalidParameter


@Resource.register
class File(Resource):
    params = {
        'content': '',
        'path': NAMEVAR,
    }

    def __init__(self, name, **params):
        super(File, self).__init__(name, **params)
        self.path = os.path.expanduser(self.path)
        if not self.path.startswith(os.sep):
            raise InvalidParameter("File paths must be fully qualified, "
                                   "not %r" % self.path)

    def __call__(self):
        exists = os.path.exists(self.path)
        content = open(self.path, 'rb').read() if exists else None

        if content != self.content:
            open(self.path, 'wb').write(self.content)
            self.logger.info("updated" if exists else "created")

            try:
                fromlines = content.decode().splitlines() if exists else []
                tolines = self.content.decode().splitlines()
            except UnicodeError:
                self.logger.info("%d bytes -> %d bytes",
                                 len(content) if exists else 0,
                                 len(self.content))
            else:
                diff = difflib.unified_diff(
                    fromlines, tolines, self.path if exists else '/dev/null',
                    self.path)
                for line in diff:
                    self.logger.debug(line.rstrip())
