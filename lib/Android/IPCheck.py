from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *
from lib.translation import *


class IPCheck(Base):
    def scan(self):
        set_values_for_key(key='ANDROIDIPCHECKTITLE', zh='IP泄露检测',
                           en='Intent component implicit call risk detection')
        set_values_for_key(key='ANDROIDIPCHECHINFO', zh='检测App泄露的IP',
                           en='Detect whether there is a risk of implicit calling of the Intent component in Apk')

        TITLE = get_value('ANDROIDIPCHECKTITLE')
        LEVEL = 1
        INFO = get_value('ANDROIDIPCHECHINFO')

        strline = cmdString("grep -r -E -o '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)' " + self.appPath)
        out = os.popen(strline).readlines()
        ips = []
        for item in out:
            if 'Binary file' in item or '0.0.0.0' in item:
                continue
            ip = item.strip().split(':')[-1]
            arr = str(ip).split('.')
            if len(arr) == 4:
                if arr[0].startswith('0') and len(arr[0]) > 1 \
                        or arr[1].startswith('0') and len(arr[1]) > 1 \
                        or arr[2].startswith('0') and len(arr[2]) > 1 \
                        or arr[3].startswith('0') and len(arr[3]) > 1:
                    continue
                # 排除小于10开头的，大概率是版本号，不是IP
                if len(arr[0]) == 1 and int(arr[0]) < 10:
                    continue
                # 排除255开头的，忽略掩码地址
                if len(arr[0]) == 3 and int(arr[0]) == 255:
                    continue
                if ip not in ips:
                    ips.append(ip)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(ips)).description()


register(IPCheck)
