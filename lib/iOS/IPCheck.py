from ..Base import Base
from ..info import Info
from ..ipa import register
from lib.translation import *


class IPCheck(Base):
    def scan(self):
        set_values_for_key(key='IOSIPCHECKTITLE', zh='IP泄露检测',
                           en='IP leak detection')
        set_values_for_key(key='IOSIPCHECKINFO', zh='检测iOS App程序中是否存在IP泄露风险',
                           en='Detect whether there is a risk of IP leakage in the iOS App')

        TITLE = get_value('IOSIPCHECKTITLE')
        LEVEL = 2
        INFO = get_value('IOSIPCHECKINFO')

        with open(self.appPath + '/IPDump', 'r') as f:
            ips = f.readlines()
            ipArr = []
            for line in ips:
                ip = line.strip()
                ipCheck = ip.split('.')
                if ipCheck[0].startswith('0') and len(ipCheck[0]) > 1 \
                        or ipCheck[1].startswith('0') and len(ipCheck[1]) > 1 \
                        or ipCheck[2].startswith('0') and len(ipCheck[2]) > 1 \
                        or ipCheck[3].startswith('0') and len(ipCheck[3]) > 1:
                    continue
                # 排除0开头的，大概率是版本号，不是IP，(0.0.0.0也忽略，没啥意义)
                if len(ipCheck[0]) == 1 and ipCheck[0] != '0':
                    continue
                # 排除小于10开头的，大概率是版本号，不是IP
                if len(ipCheck[0]) == 1 and int(ipCheck[0]) < 10:
                    continue
                # 排除255开头的，忽略掩码地址
                if len(ipCheck[0]) == 3 and int(ipCheck[0]) == 255:
                    continue
                # 排除四个数相等的，大概率是DNS服务器地址
                if ipCheck[0] == ipCheck[1] and ipCheck[1] == ipCheck[2] and ipCheck[2] == ipCheck[3]:
                    continue
                if ip not in ipArr:
                    ipArr.append(ip)
            Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO,
                 result='\n'.join(ipArr)).description()


register(IPCheck)
