from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *
from lib.translation import *


class URLCheck(Base):
    def scan(self):
        set_values_for_key(key='ANDROIDURLCHECKTITLE', zh='URL泄露检测',
                           en='URL leak detection')
        set_values_for_key(key='ANDROIDURLCHECHINFO', zh='检测App泄露的URL',
                           en="Detect URL leaked by App")

        TITLE = get_value('ANDROIDURLCHECKTITLE')
        LEVEL = 1
        INFO = get_value('ANDROIDURLCHECHINFO')

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