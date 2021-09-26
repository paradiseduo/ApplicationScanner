from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *
from lib.translation import *


class BroadcastCheck(Base):
    def scan(self):
        set_values_for_key(key='BROADCASTCHECKTITLE', zh='Broadcast Receiver动态注册检测',
                           en='Broadcast Receiver dynamic registration detection')
        set_values_for_key(key='BROADCASTCHECHINFO', zh='检测App中是否存在动态注册Receiver风险',
                           en='Detect whether there is a risk of dynamically registering Receiver in the App')

        TITLE = get_value('BROADCASTCHECKTITLE')
        LEVEL = 1
        INFO = get_value('BROADCASTCHECHINFO')

        strline = cmdString('grep -r "registerReceiver(Landroid/content/BroadcastReceiver;Landroid/content/IntentFilter;)Landroid/content/Intent" ' + self.appPath)
        paths = getSmalis(os.popen(strline).readlines())
        results = []
        for path in paths:
            with open(path, 'r') as f:
                lines = f.readlines()
                count = len(lines)
                name = getFileName(path)
                for i in range(0, count):
                    line = lines[i]
                    if '->registerReceiver(Landroid/content/BroadcastReceiver;Landroid/content/IntentFilter;)Landroid/content/Intent' in line:
                        result = name + ' : ' + str(i + 1)
                        if result not in results:
                            results.append(result)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(BroadcastCheck)