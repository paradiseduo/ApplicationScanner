from ..Base import Base
from ..info import Info
from ..ipa import register

TITLE = 'XcodeGhost感染检测'
LEVEL = 3
INFO = '检测iOS App中是否被植入XcodeGhost恶意代码'


class XcodeGhostCheck(Base):
    def scan(self):
        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().upper()
                if 'init.icloud-analysis.com' in line:
                    Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='iOS App中被植入XcodeGhost恶意代码').description()
                    break


register(XcodeGhostCheck)
