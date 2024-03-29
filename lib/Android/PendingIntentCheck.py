from lib.translation import *
from ..Base import Base
from ..apk import register
from ..info import Info
from ..tools import *


class PendingIntentCheck(Base):
    def scan(self):
        set_values_for_key(key='PENDINGCHECKTITLE', zh='PendingIntent错误使用Intent风险检测',
                           en='PendingIntent wrong use of Intent risk detection')
        set_values_for_key(key='PENDINGCHECHINFO',
                           zh='检测App中是否存在PendingIntent使用了隐式Intent或者空Intent的风险',
                           en='Detect whether there is a risk of PendingIntent using implicit Intent or empty Intent in App')

        TITLE = get_value('PENDINGCHECKTITLE')
        LEVEL = 1
        INFO = get_value('PENDINGCHECHINFO')

        strline = cmdString(f'grep -r "Landroid/app/PendingIntent;" {self.appPath}')
        paths = getSmalis(os.popen(strline).readlines())
        results = []
        for path in paths:
            with open(path, 'r') as f:
                lines = f.readlines()
                lines.reverse()
                count = len(lines)
                name = getFileName(path)
                for index, line in enumerate(lines):
                    if 'Landroid/app/PendingIntent;->get' in line and 'Landroid/content/Intent;' in line:
                        v = line.strip().split(',')[2].replace(' ', '')
                        for i in range(index, count):
                            s = lines[i]
                            if v in s:
                                if 'Landroid/content/Intent;->setAction' in s or \
                                            'Landroid/content/Intent;->setClass' in s or \
                                            'Landroid/content/Intent;->setClassName' in s or \
                                            'Landroid/content/Intent;->setComponent' in s or \
                                            'Landroid/content/Intent;->setPackage' in s or \
                                            'Landroid/content/Intent;-><init>(Ljava/lang/String;)V' in s:
                                    break
                                if 'Landroid/content/Intent;-><init>()V' in s:
                                    result = f'{name} : {str(count - index)}'
                                    if result not in results:
                                        results.append(result)
                                    break
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(PendingIntentCheck)
