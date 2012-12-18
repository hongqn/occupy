from subprocess import check_call

from occupy.resource import Resource

@Resource.register('cmd')
class Command(Resource):
    def __call__(self):
        check_call(self.name, shell=True)
        self.logger.info("executed successfully")
