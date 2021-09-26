from ..Base import Base
from ..info import Info
from ..ipa import register
import json
from lib.translation import *


class CanaryCheck(Base):
    def scan(self):
        set_values_for_key(key='CANARYCHECKTITLE', zh='编译器堆栈保护技术检测',
                           en='Compiler stack protection technology detection')
        set_values_for_key(key='CANARYCHECKINFO', zh='检测iOS App程序中是否存在未使用编译器堆栈保护技术风险',
                           en='Detect whether there is a risk of unused compiler stack protection technology in the iOS App program')
        set_values_for_key(key='CANARYCHECKRESULT', zh='该App程序中未使用编译器堆栈保护技术',
                           en='Compiler stack protection technology is not used in the App program')

        TITLE = get_value('CANARYCHECKTITLE')
        LEVEL = 1
        INFO = get_value('CANARYCHECKINFO')
        with open(self.appPath + '/macho.json', 'r') as f:
            dic = json.loads(f.read())
            if not dic['has_canary']:
                Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result=get_value('CANARYCHECKRESULT')).description()


register(CanaryCheck)
