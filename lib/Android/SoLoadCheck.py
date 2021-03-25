from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *

TITLE = 'SDCARD加载so检测'
LEVEL = 1
INFO = '检测App程序中的是否存在从sdcard动态加载so的风险'


class SoLoadCheck(Base):
    def scan(self):
        strline = cmdString(
            'grep -r "Ljava/lang/System;->load(Ljava/lang/String;)V" ' + self.appPath)
        paths = getSmalis(os.popen(strline).readlines())
        results = []
        for path in paths:
            with open(path, 'r') as f:
                lines = f.readlines()
                lines.reverse()
                count = len(lines)
                name = getFileName(path)
                for i in range(0, count):
                    line = lines[i]
                    if 'Ljava/lang/System;->load(Ljava/lang/String;)V' in line:
                        for j in range(i, count):
                            ll = lines[j]
                            if 'Landroid/os/Environment;->getExternalStorageDirectory' in ll:
                                for k in range(i, j):
                                    lll = lines[k]
                                    if 'Ljava/io/File;->toString()Ljava/lang/String' in lll:
                                        vs = lll.find('{') + 1
                                        ve = lll.find('}')
                                        v = lll[vs:ve]
                                        if v in line:
                                            result = name + ' : ' + str(count - i)
                                            if result not in results:
                                                results.append(result)
                                            break
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(SoLoadCheck)
