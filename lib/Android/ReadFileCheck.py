from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *

TITLE = '全局可读写风险检测'
LEVEL = 1
INFO = '检测App的SharedPreferences,getDir,openFileOutput函数是否存在全局可读写风险'


class ReadFileCheck(Base):
    def scan(self):
        strline = cmdString('grep -r "getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences\|Landroid/content/Context;->getDir\|Landroid/content/Context;->openFileOutput" ' + self.appPath)
        paths = getSmalis(os.popen(strline).readlines())
        results = []
        for path in paths:
            with open(path, 'r') as f:
                lines = f.readlines()
                count = len(lines)
                name = getFileName(path)
                for i in range(0, count):
                    line = lines[i]
                    if 'getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences' in line or \
                            'Landroid/content/Context;->openFileOutput' in line or \
                            'Landroid/content/Context;->getDir' in line:
                        v = line.strip().split(',')[2].replace('}', '')
                        for j in range(i, count):
                            ll = lines[j]
                            if v in ll and 'const/4' in ll:
                                value = ll.strip().split(' ')[-1]
                                if value != '0x0':
                                    result = name + ' : ' + str(count - i)
                                    if result not in results:
                                        results.append(result)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(ReadFileCheck)