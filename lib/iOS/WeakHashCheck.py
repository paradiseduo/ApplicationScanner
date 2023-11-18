from lib.translation import *
from ..Base import Base
from ..info import Info
from ..ipa import register


class WeakHashCheck(Base):
    def scan(self):
        set_values_for_key(key='WEAKHASHCHECKTITLE', zh='弱哈希算法检测',
                           en='Weak hash algorithm detection')
        set_values_for_key(key='WEAKHASHCHECKINFO', zh='检测iOS App程序中是否使用了不安全的弱哈希算法',
                           en='Detect whether an insecure weak hash algorithm is used in the iOS App')

        TITLE = get_value('WEAKHASHCHECKTITLE')
        LEVEL = 1
        INFO = get_value('WEAKHASHCHECKINFO')

        results = []
        with open(f'{self.appPath}/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if (
                        line
                        in [
                    '@_CC_SHA1_Final',
                    '@_CC_SHA1_Init',
                    '@_CC_SHA1_Update',
                    '@_CC_SHA1',
                ]
                        and line not in results
                ):
                    results.append(line)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(WeakHashCheck)
