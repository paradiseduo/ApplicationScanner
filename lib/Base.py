import traceback


class Base:
    def __init__(self, appPath, appBinPath="", **kwargs):
        self._appPath = appPath
        self._appBinPath = appBinPath
        self._kwargs = kwargs

    @property
    def appPath(self):
        return self._appPath

    @property
    def appBinPath(self):
        return self._appBinPath

    def scan(self):
        raise NotImplementedError("该方法必须在子类重写!")

    def __call__(self, *args, **kwargs):
        return self.scan()
