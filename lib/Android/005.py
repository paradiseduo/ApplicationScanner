from ..Base import Base
from ..info import Info
from ..tools import *
from ..apk import register

TITLE = 'Fragment注入攻击检测'
LEVEL = 3
INFO = '检测Apk中是否存在Fragment注入攻击'


class FragmentCheck(Base):
    def scan(self):
        strline = cmdString('grep -r "Landroid/preference/PreferenceActivity" ' + self.appPath)
        arr = os.popen(strline).readlines()
        results = []
        for item in arr:
            path = item.split(':')[0]
            with open(path, 'r') as f:
                lines = f.readlines()
                index = 0
                count = len(lines)
                isExp = True
                for line in lines:
                    index += 1
                    if '.method protected isValidFragment(Ljava/lang/String;)Z' in line:
                        for i in range(index, count):
                            p = lines[i]
                            if 'if-ne' in p:
                                isExp = False
                            if 'Landroid/preference/PreferenceActivity;->isValidFragment(Ljava/lang/String;)Z' in p:
                                break
                if isExp:
                    result = getFileName(path)
                    if result not in results:
                        results.append(result)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(FragmentCheck)