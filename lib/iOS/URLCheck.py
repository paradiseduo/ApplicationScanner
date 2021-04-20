from ..Base import Base
from ..info import Info
from ..ipa import register

TITLE = 'HTTP传输数据风险检测'
LEVEL = 2
INFO = '检测iOS App程序是否使用未加密的HTTP协议传输数据'


class URLCheck(Base):
    def scan(self):
        results = []
        with open(self.appPath + '/URLDump', 'r') as f:
            lines = f.readlines()
            for url in lines:
                url = url.strip()
                if 'http://' in url and len(url) > 11 and url not in results:
                    results.append(url)
            Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(URLCheck)
