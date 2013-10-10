from subprocess import check_call

from occupy.resource import Resource, NAMEVAR


class Command(Resource):
    def __init__(self, name, command=NAMEVAR):
        super(Command, self).__init__(name)
        self.command = command or self.name

    def __call__(self):
        check_call(self.command, shell=True)
        self.logger.info("executed successfully")
