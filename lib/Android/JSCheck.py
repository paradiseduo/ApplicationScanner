from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *
from lib.translation import *


class JSCheck(Base):
    def scan(self):
        set_values_for_key(key='ANDROIDJSCHECKTITLE', zh='JavaScript资源文件泄露检测',
                           en='JavaScript resource file leak detection')
        set_values_for_key(key='ANDROIDJSCHECHINFO', zh='检测Apk中是否存在JavaScript文件信息泄露风险',
                           en='Detect whether there is a risk of JavaScript file information leakage in Apk')

        TITLE = get_value('ANDROIDJSCHECKTITLE')
        LEVEL = 1
        INFO = get_value('ANDROIDJSCHECHINFO')

        strline = cmdString("find " + self.appPath + " -name '*.js'")
        out = os.popen(strline).readlines()
        jsfiles = []
        for line in out:
            filepath = line[:-1]
            if filepath not in jsfiles:
                jsfiles.append(filepath)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(jsfiles)).description()


register(JSCheck)