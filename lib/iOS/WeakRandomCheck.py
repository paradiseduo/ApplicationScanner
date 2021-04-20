from ..Base import Base
from ..info import Info
from ..ipa import register

TITLE = '随机数不安全使用检测'
LEVEL = 1
INFO = '检测iOS App程序中是否存在随机数可被猜解的漏洞'


class WeakRandomCheck(Base):
    def scan(self):
        results = []
        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().lower()
                if ('@_rand' == line or '@_random' == line) and line not in results:
                    results.append(line)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(WeakRandomCheck)
