class Facter:
    _system = None

    @property
    def system(self):
        if self._system is None:
            import platform
            self._system = platform.system()
        return self._system


facts = Facter()
