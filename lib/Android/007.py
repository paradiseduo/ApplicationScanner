from ..Base import Base
from ..info import Info
from ..tools import *
from ..apk import register

TITLE = '日志泄漏风险检测'
LEVEL = 1
INFO = '检测Apk中是否存在日志泄露风险，重点检测Log与print函数'


class LogCheck(Base):
    def scan(self):
        strline = cmdString('grep -r "Landroid/util/Log\|Ljava/io/PrintStream" ' + self.appPath)
        arr = os.popen(strline).readlines()
        results = []
        for item in arr:
            if '.smali:' in item:
                path = item.split(':')[0]
                with open(path, 'r') as f:
                    lines = f.readlines()
                    index = 0
                    name = getFileName(path)
                    for line in lines:
                        index += 1
                        if 'Landroid/util/Log;->d' in line or 'Landroid/util/Log;->v' in line or 'Ljava/io/PrintStream;->print' in line:
                            result = name + ' : ' + str(index)
                            if result not in results:
                                results.append(result)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(LogCheck)