from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *

TITLE = '剪切板敏感信息泄露检测'
LEVEL = 2
INFO = '检测App是否存在剪切板敏感数据泄露风险'


class ClipboardCheck(Base):
    def scan(self):
        strline = cmdString('grep -r "ClipboardManager;->setPrimaryClip\|ClipboardManager;->setText" ' + self.appPath)
        arrs = os.popen(strline).readlines()
        results = []
        for item in arrs:
            if '.smali:' in item:
                path = item.split(':')[0]
                with open(path, 'r') as f:
                    lines = f.readlines()
                    lines.reverse()
                    count = len(lines)
                    name = getFileName(path)
                    for i in range(0, count):
                        line = lines[i]
                        if 'ClipboardManager;->setPrimaryClip' in line or 'ClipboardManager;->setText' in line:
                            result = name + ' : ' + str(count - i)
                            if result not in results:
                                results.append(result)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(ClipboardCheck)