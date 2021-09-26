from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *
from lib.translation import *


class SQLInjectCheck(Base):
    def scan(self):
        set_values_for_key(key='SQLCHECKTITLE', zh='SQL注入检测',
                           en='SQL injection detection')
        set_values_for_key(key='SQLCHECHINFO', zh='检测App是否存在SQL注入的利用条件',
                           en="Detect whether there are usage conditions for SQL injection in the App")

        TITLE = get_value('SQLCHECKTITLE')
        LEVEL = 2
        INFO = get_value('SQLCHECHINFO')

        strline = cmdString('grep -r "Landroid/database/sqlite/SQLiteDatabase" ' + self.appPath)
        paths = getSmalis(os.popen(strline).readlines())
        results = []
        for path in paths:
            with open(path, 'r') as f:
                lines = f.readlines()
                count = len(lines)
                name = getFileName(path)
                for i in range(0, count):
                    line = lines[i]
                    if '?' in line and 'const-string' in line:
                        v = line.strip().split(' ')[1]
                        for j in range(i, count):
                            ll = lines[j]
                            if v in ll and (
                                    'Landroid/database/sqlite/SQLiteDatabase;->rawQuery' in ll or 'Landroid/database/sqlite/SQLiteDatabase;->execSQL' in ll):
                                result = name + ' : ' + str(j + 1)
                                if result not in results:
                                    results.append(result)
                                break
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(SQLInjectCheck)