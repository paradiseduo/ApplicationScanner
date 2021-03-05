from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *

TITLE = '测试URL泄露检测'
LEVEL = 1
INFO = '检测App泄露的URL'


class URLCheck(Base):
    def scan(self):
        strline = cmdString('grep -r -Eo \'(http|https)://[^/"]+\' ' + self.appPath)
        out = os.popen(strline).readlines()
        urls = []
        for item in out:
            if 'Binary file' in item or 'schemas.android.com' in item or 'android.googlesource.com' in item:
                continue
            url = item.strip().split(':http')[-1]
            if not url.startswith('http'):
                url = 'http' + url
            if url not in urls and '.' in url:
                urls.append(url)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(urls)).description()


register(URLCheck)