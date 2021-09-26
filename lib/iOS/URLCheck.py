from ..Base import Base
from ..info import Info
from ..ipa import register
from lib.translation import *


class URLCheck(Base):
    def scan(self):
        set_values_for_key(key='IOSURLCHECKTITLE', zh='HTTP传输数据风险检测',
                           en='HTTP transmission data risk detection')
        set_values_for_key(key='IOSURLCHECKINFO', zh='检测iOS App程序是否使用未加密的HTTP协议传输数据',
                           en='Detect whether the iOS App program uses unencrypted HTTP protocol to transmit data')

        TITLE = get_value('IOSURLCHECKTITLE')
        LEVEL = 2
        INFO = get_value('IOSURLCHECKINFO')

        results = []
        with open(self.appPath + '/URLDump', 'r') as f:
            lines = f.readlines()
            for url in lines:
                url = url.strip()
                if 'http://' in url and len(url) > 11 and url not in results:
                    results.append(url)
            Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(URLCheck)
