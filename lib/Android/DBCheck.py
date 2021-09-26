from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *
from lib.translation import *


class DBCheck(Base):
    def scan(self):
        set_values_for_key(key='DBCHECKTITLE', zh='数据库文件任意读写检测',
                           en='Arbitrary read and write detection of database files')
        set_values_for_key(key='DBCHECHINFO', zh='检测App是否存在数据库文件任意读写风险',
                           en='Detect whether the app has the risk of sensitive data leakage on the clipboard')

        TITLE = get_value('DBCHECKTITLE')
        LEVEL = 2
        INFO = get_value('DBCHECHINFO')

        strline = cmdString('grep -r "Landroid/content/Context;->openOrCreateDatabase" ' + self.appPath)
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