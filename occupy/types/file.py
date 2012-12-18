import os

from occupy.resource import Resource, InvalidParameter, NAMEVAR

@Resource.register('file')
class File(Resource):
    params = {
        'content': '',
        'path': NAMEVAR,
    }

    def __call__(self):
        if os.path.exists(self.path):
            current_content = open(self.name, 'rb').read()
