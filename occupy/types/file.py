import os
import difflib

from occupy.resource import Resource, IDVAR, InvalidParameter


class File(Resource):
    def __init__(self, id, path=IDVAR, content='', **meta):
        super().__init__(id, **meta)
        self.path = os.path.expanduser(path or id)
        if not self.path.startswith(os.sep):
            raise InvalidParameter("File paths must be fully qualified, "
                                   "not %r" % self.path)
        self.content = content

    def apply(self):
        exists = os.path.exists(self.path)
        content = open(self.path, 'rb').read() if exists else None

        if content != self.content:
            self.update(content)
        else:
            self.logger.debug("%s does not change", self.path)

    def update(self, content):
        exists = content is not None

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
