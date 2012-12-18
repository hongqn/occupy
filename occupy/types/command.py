from subprocess import check_call

from occupy.resource import Resource, NAMEVAR

@Resource.register('command')
class Command(Resource):
    params = {
        'command': NAMEVAR,
    }

    def __call__(self):
        check_call(self.command, shell=True)
        self.logger.info("executed successfully")
