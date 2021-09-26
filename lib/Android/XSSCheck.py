from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *
from lib.translation import *


class XSSCheck(Base):
    def scan(self):
        set_values_for_key(key='XSSCHECKTITLE', zh='WebView明文存储密码检测',
                           en="InnerHTML's XSS vulnerability detection")
        set_values_for_key(key='XSSDCHECHINFO', zh='检测App程序是否存在WebView明文存储密码风险',
                           en="Detect whether the App program has the risk of WebView storing passwords in plain text")

        TITLE = get_value('XSSCHECKTITLE')
        LEVEL = 1
        INFO = get_value('XSSDCHECHINFO')

        strline = cmdString("find " + self.appPath + " -name '*.js'")
        out = os.popen(strline).readlines()
        jsfiles = []
        for line in out:
            filepath = line[:-1]
            if filepath not in jsfiles:
                jsfiles.append(filepath)
        files = jsBeautify(jsfiles)
        results = []
        for item in files:
            with open(item, 'r') as f:
                io = f.read()
                s = str(io)
                if 'innerHTML' in s:
                    results += item.replace('1.js', '.js')
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result=''.join(results)).description()


register(XSSCheck)
