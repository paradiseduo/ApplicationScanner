from ..Base import Base
from ..info import Info
from ..ipa import register

TITLE = '弱哈希算法检测'
LEVEL = 1
INFO = '检测iOS App程序中是否使用了不安全的弱哈希算法'


class WeakHashCheck(Base):
    def scan(self):
        results = []
        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if ('@_CC_SHA1_Final' == line or '@_CC_SHA1_Init' == line or '@_CC_SHA1_Update' == line or '@_CC_SHA1' == line) and line not in results:
                    results.append(line)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(WeakHashCheck)
