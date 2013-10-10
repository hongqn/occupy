from subprocess import getstatusoutput, CalledProcessError

from occupy.resource import Resource, IDVAR, InvalidParameter


class Cmd(Resource):
    def __init__(self, id, command=IDVAR, unless=None, onlyif=None, **meta):
        super().__init__(id, **meta)
        self.command = command or self.id
        self.unless = unless
        self.onlyif = onlyif

    def apply(self):
        to_run = self.check_condition()
        if not to_run:
            self.logger.debug("no need to run")
            return

        retcode, output = getstatusoutput(self.command)
        if retcode != 0:
            self.logger.warning(output)
            raise CalledProcessError(retcode, self.command, output=output)
        self.logger.info("executed successfully")

    def check_condition(self):
        onlyif = self._eval_condition(self.onlyif)
        unless = self._eval_condition(self.unless)

        conditions = {}
        if onlyif is not None:
            conditions['onlyif'] = onlyif
        if unless is not None:
            conditions['unless'] = not unless

        if not conditions:
            # no condition specified
            return True

        to_run = set(conditions.values())
        if len(to_run) != 1:
            # condition conflicts
            raise InvalidParameter("conflict conditions: {}".format(
                conditions.keys()))

        return to_run.pop()

    def _eval_condition(self, condition):
        if condition is None:
            return None

        if callable(condition):
            return bool(condition())
        elif isinstance(condition, str):
            return getstatusoutput(condition)[0] == 0
        else:
            return bool(condition)
