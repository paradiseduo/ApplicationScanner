from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *

TITLE = 'Java反射检测'
LEVEL = 1
INFO = '检测App程序是否存在反射调用风险'


class ReflectCheck(Base):
    def scan(self):
        strline = cmdString(
            'grep -r "Ljava/lang/reflect/" ' + self.appPath)
        arrs = os.popen(strline).readlines()
        results = []
        for item in arrs:
            if '.smali:' in item:
                path = item.split(':')[0]
                with open(path, 'r') as f:
                    lines = f.readlines()
                    lines.reverse()
                    count = len(lines)
                    name = getFileName(path)
                    for i in range(0, count):
                        line = lines[i]
                        if 'Ljava/lang/reflect/' in line:
                            result = name + ' : ' + str(i + 1)
                            if result not in results:
                                results.append(result)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(ReflectCheck)
