from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *

TITLE = '数据库文件任意读写检测'
LEVEL = 2
INFO = '检测App是否存在数据库文件任意读写风险'


class DBCheck(Base):
    def scan(self):
        strline = cmdString('grep -r "Landroid/content/Context;->openOrCreateDatabase" ' + self.appPath)
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
                        if 'Landroid/content/Context;->openOrCreateDatabase' in line:
                            v = line.split(',')[2]
                            for j in range(i, count):
                                ll = lines[j]
                                if 'const/4' in ll and v in ll:
                                    value = ll.strip().split(' ')[-1]
                                    if value != '0x0':
                                        result = name + ' : ' + str(count - i)
                                        if result not in results:
                                            results.append(result)
                                    break
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(DBCheck)