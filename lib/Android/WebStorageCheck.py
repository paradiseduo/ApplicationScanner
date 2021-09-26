from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *
from lib.translation import *


class WebStorageCheck(Base):
    def scan(self):
        set_values_for_key(key='WEBSTOROAGECHECKTITLE', zh='WEB STORAGE数据泄露检测',
                           en='WEB STORAGE data leakage detection')
        set_values_for_key(key='WEBSTORAGECHECHINFO', zh='检测App是否存在Web Storage数据泄露风险',
                           en="Detect whether there is a risk of Web Storage data leakage in the App")

        TITLE = get_value('WEBSTOROAGECHECKTITLE')
        LEVEL = 1
        INFO = get_value('WEBSTORAGECHECHINFO')

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
                if 'localStorage' in s or 'sessionStorage' in s:
                    results += item.replace('1.js', '.js')
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result=''.join(results)).description()


register(WebStorageCheck)