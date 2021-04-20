from ..Base import Base
from ..info import Info
from ..ipa import register

TITLE = '创建可执行权限内存风险检测'
LEVEL = 2
INFO = '检测iOS App程序中是否存在创建可执行内存的风险'


class MprotectCheck(Base):
    def scan(self):
        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().lower()
                if '@_mprotec' in line:
                    Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='iOS App程序中存在创建可执行内存的风险').description()
                    break


register(MprotectCheck)
