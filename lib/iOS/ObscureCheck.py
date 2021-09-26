from ..Base import Base
from ..info import Info
from ..ipa import register
from lib.translation import *

blackList = ['Login', 'Helper', 'Manager']


class ObscureCheck(Base):
    def scan(self):
        set_values_for_key(key='OBSCURECHECKTITLE', zh='代码未混淆风险检测',
                           en='Code unobfuscated risk detection')
        set_values_for_key(key='OBSCURECHECKINFO', zh='检测iOS App程序的源代码是否已经经过混淆处理',
                           en='Check whether the source code of the iOS App has been obfuscated')

        TITLE = get_value('OBSCURECHECKTITLE')
        LEVEL = 1
        INFO = get_value('OBSCURECHECKINFO')

        results = []
        with open(self.appPath+'/ClassDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                for s in blackList:
                    if s in line and line not in results:
                        results.append(line)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result="\n".join(results)).description()


register(ObscureCheck)
