from ..Base import Base
from ..info import Info
from ..ipa import register

TITLE = '调试日志函数调用风险检测'
LEVEL = 1
INFO = '检测iOS App程序中是否调用了调试日志函数'


class NSLogCheck(Base):
    def scan(self):
        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if '@_NSLog' in line or '@_NSLogv' in line:
                    Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='该App程序中调用了调试日志函数NSLog').description()
                    break


register(NSLogCheck)
