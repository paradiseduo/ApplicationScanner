from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *
from lib.translation import *


class ClipboardCheck(Base):
    def scan(self):
        set_values_for_key(key='CLIPCHECKTITLE', zh='剪切板敏感信息泄露检测',
                           en='Clipboard sensitive information leakage detection')
        set_values_for_key(key='CLIPCHECHINFO', zh='检测App是否存在剪切板敏感数据泄露风险',
                           en='Detect whether the app has the risk of sensitive data leakage on the clipboard')

        TITLE = get_value('CLIPCHECKTITLE')
        LEVEL = 2
        INFO = get_value('CLIPCHECHINFO')

        strline = cmdString('grep -r "ClipboardManager;->setPrimaryClip\|ClipboardManager;->setText" ' + self.appPath)
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
                    if 'ClipboardManager;->setPrimaryClip' in line or 'ClipboardManager;->setText' in line:
                        result = name + ' : ' + str(count - i)
                        if result not in results:
                            results.append(result)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(ClipboardCheck)