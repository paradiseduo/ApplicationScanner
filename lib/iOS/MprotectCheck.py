from ..Base import Base
from ..info import Info
from ..ipa import register
from lib.translation import *


class MprotectCheck(Base):
    def scan(self):
        set_values_for_key(key='MPROTECTCHECKTITLE', zh='创建可执行权限内存风险检测',
                           en='Create executable permission memory risk detection')
        set_values_for_key(key='MPROTECTCHECKINFO', zh='检测iOS App程序中是否存在创建可执行内存的风险',
                           en='Detect whether there is a risk of creating executable memory in the iOS App')
        set_values_for_key(key='MPROTECTCHECKRESULT', zh='iOS App程序中存在创建可执行内存的风险',
                           en='There is a risk of creating executable memory in the iOS App')

        TITLE = get_value('MPROTECTCHECKTITLE')
        LEVEL = 2
        INFO = get_value('MPROTECTCHECKINFO')

        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().lower()
                if '@_mprotec' in line:
                    Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result=get_value('MPROTECTCHECKRESULT')).description()
                    break


register(MprotectCheck)
