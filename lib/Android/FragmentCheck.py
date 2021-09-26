from ..Base import Base
from ..info import Info
from ..tools import *
from ..apk import register
from lib.translation import *


class FragmentCheck(Base):
    def scan(self):
        set_values_for_key(key='FRAGMENTCHECKTITLE', zh='Fragment注入攻击检测',
                           en='Fragment injection attack detection')
        set_values_for_key(key='FRAGMENTCHECHINFO', zh='检测Apk中是否存在Fragment注入攻击',
                           en='Detect whether there is a Fragment injection attack in Apk')

        TITLE = get_value('FRAGMENTCHECKTITLE')
        LEVEL = 3
        INFO = get_value('FRAGMENTCHECHINFO')

        strline = cmdString('grep -r "Landroid/preference/PreferenceActivity" ' + self.appPath)
        paths = getSmalis(os.popen(strline).readlines())
        results = []
        for path in paths:
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