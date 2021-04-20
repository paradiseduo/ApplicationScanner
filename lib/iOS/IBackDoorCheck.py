from ..Base import Base
from ..info import Info
from ..ipa import register

TITLE = 'iBackDoor控制漏洞检测'
LEVEL = 3
INFO = '检测iOS App中是否存在可被远程控制的iBackDoor漏洞'


class IBackDoorCheck(Base):
    def scan(self):
        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if 'mobiSage' in line:
                    Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='iOS App中存在可被远程控制的iBackDoor漏洞').description()
                    break


register(IBackDoorCheck)
