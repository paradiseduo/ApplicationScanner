from ..Base import Base
from ..info import Info
from ..ipa import register
import json

TITLE = '编译器堆栈保护技术检测'
LEVEL = 1
INFO = '检测iOS App程序中是否存在未使用编译器堆栈保护技术风险'


class CanaryCheck(Base):
    def scan(self):
        with open(self.appPath + '/macho.json', 'r') as f:
            dic = json.loads(f.read())
            if not dic['has_canary']:
                Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='该App程序中未使用编译器堆栈保护技术').description()


register(CanaryCheck)
