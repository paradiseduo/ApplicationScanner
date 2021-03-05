from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *

TITLE = 'JS资源文件泄露检测'
LEVEL = 1
INFO = '检测Apk中是否存在JS文件信息泄露风险'


class JSCheck(Base):
    def scan(self):
        strline = cmdString("find " + self.appPath + " -name '*.js'")
        out = os.popen(strline).readlines()
        jsfiles = []
        for line in out:
            filepath = line[:-1]
            if filepath not in jsfiles:
                jsfiles.append(filepath)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(jsfiles)).description()


register(JSCheck)