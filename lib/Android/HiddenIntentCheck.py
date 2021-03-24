from ..Base import Base
from ..info import Info
from ..tools import *
from ..apk import register

TITLE = 'Intent组件隐式调用风险'
LEVEL = 1
INFO = '检测Apk中的Intent组件是否存在隐式调用的风险'


class HiddenIntentCheck(Base):
    def scan(self):
        strline = cmdString('grep -r "Landroid/content/Intent;-><init>" ' + self.appPath)
        paths = getSmalis(os.popen(strline).readlines())
        results = []
        for path in paths:
            with open(path, 'r') as f:
                lines = f.readlines()
                lines.reverse()
                index = 0
                count = len(lines)
                name = getFileName(path)
                for line in lines:
                    if ';->startActivit' in line and 'Landroid/content/Intent' in line:
                        v = line.strip().split(',')[1].strip().replace('}', '')
                        for i in range(index, count):
                            ll = lines[i]
                            if v in ll:
                                if 'Landroid/content/Intent;->setComponent' in ll or \
                                        'Landroid/content/Intent;->setClass' in ll or \
                                        'Landroid/content/Intent;->setClassName' in ll or \
                                        'Landroid/content/Intent;->setPackage' in ll:
                                    break
                                if 'Landroid/content/Intent' in ll and 'new-instance' in ll:
                                    result = name + ' : ' + str(count - index)
                                    if result not in results:
                                        results.append(result)
                                    break
                    index += 1
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(HiddenIntentCheck)