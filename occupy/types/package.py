from shutil import which

from occupy.resource import Resource
from .cmd import Cmd


class Eix:
    def __new__(cls):
        yield Cmd("emerge app-portage/eix",
                  unless=lambda: which("eix"))


class Package(Resource):
    def apply(self):
        yield Eix
        yield Cmd(self.s("emerge {id}"),
                  unless=self.s("eix -I -e {id}"),
                  require=Cmd["emerge app-portage/eix"])
