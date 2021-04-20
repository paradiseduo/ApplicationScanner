from ..Base import Base
from ..info import Info
from ..ipa import register

TITLE = '内存分配函数不安全风险检测'
LEVEL = 1
INFO = '检测iOS App程序中是否不安全的调用了内存分配函数'


class MallocCheck(Base):
    def scan(self):
        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().lower()
                if '@_malloc' in line:
                    Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='iOS App程序中不安全的调用了内存分配函数').description()
                    break


register(MallocCheck)
