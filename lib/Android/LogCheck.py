from ..Base import Base
from ..info import Info
from ..tools import *
from ..apk import register
from lib.translation import *


class LogCheck(Base):
    def scan(self):
        set_values_for_key(key='ANDROIDLOGCHECKTITLE', zh='日志泄漏风险检测',
                           en='JavaScript resource file leak detection')
        set_values_for_key(key='ANDROIDLOGCHECHINFO', zh='检测Apk中是否存在日志泄露风险，重点检测Log与print函数',
                           en='Detect whether there is a risk of JavaScript file information leakage in Apk')

        TITLE = get_value('ANDROIDLOGCHECKTITLE')
        LEVEL = 1
        INFO = get_value('ANDROIDLOGCHECHINFO')

        strline = cmdString('grep -r "Landroid/util/Log\|Ljava/io/PrintStream" ' + self.appPath)
        paths = getSmalis(os.popen(strline).readlines())
        results = []
        for path in paths:
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