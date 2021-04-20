from ..Base import Base
from ..info import Info
from ..ipa import register

TITLE = '未使用自动管理内存技术风险检测'
LEVEL = 1
INFO = '检测iOS App程序中是否存在未使用自动管理内存技术风险'


class ARCCheck(Base):
    def scan(self):
        hasBug = True
        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if '_autoreleasePool' in line or '_objc_autorelease' in line or 'autorelease' in line:
                    hasBug = False
                    break
        if hasBug:
            Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='iOS App程序中存在未使用自动管理内存技术风险').description()


register(ARCCheck)
