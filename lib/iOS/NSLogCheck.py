from ..Base import Base
from ..info import Info
from ..ipa import register
from lib.translation import *


class NSLogCheck(Base):
    def scan(self):
        set_values_for_key(key='LOGCHECKTITLE', zh='调试日志函数调用风险检测',
                           en='Debug log function call risk detection')
        set_values_for_key(key='LOGCHECKINFO', zh='检测iOS App程序中是否调用了调试日志函数',
                           en='Detect whether the debug log function is called in the iOS App program')
        set_values_for_key(key='LOGCHECKRESULT', zh='该App程序中调用了调试日志函数NSLog',
                           en='The debug log function NSLog is called in the App program')

        TITLE = get_value('LOGCHECKTITLE')
        LEVEL = 1
        INFO = get_value('LOGCHECKINFO')

        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if '@_NSLog' in line or '@_NSLogv' in line:
                    Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result=get_value('LOGCHECKRESULT')).description()
                    break


register(NSLogCheck)
