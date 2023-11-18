from lib.translation import *
from ..Base import Base
from ..info import Info
from ..ipa import register


class WeakRandomCheck(Base):
    def scan(self):
        set_values_for_key(key='WEAKRANDOMCHECKTITLE', zh='随机数不安全使用检测',
                           en='Random number insecure use detection')
        set_values_for_key(key='WEAKRANDOMCHECKINFO', zh='检测iOS App程序中是否存在随机数可被猜解的漏洞',
                           en='Detect whether there are vulnerabilities in which random numbers can be guessed in the iOS App')

        TITLE = get_value('WEAKRANDOMCHECKTITLE')
        LEVEL = 1
        INFO = get_value('WEAKRANDOMCHECKINFO')

        results = []
        with open(f'{self.appPath}/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().lower()
                if line in ['@_rand', '@_random'] and line not in results:
                    results.append(line)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(WeakRandomCheck)
