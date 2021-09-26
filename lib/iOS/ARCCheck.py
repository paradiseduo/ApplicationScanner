from ..Base import Base
from ..info import Info
from ..ipa import register
from lib.translation import *

class ARCCheck(Base):
    def scan(self):
        set_values_for_key(key='ARCCHECKTITLE', zh='未使用自动管理内存技术风险检测', en='Risk detection without automatic memory management technology')
        set_values_for_key(key='ARCCHECKINFO', zh='检测iOS App程序中是否存在未使用自动管理内存技术风险',
                           en='Detect whether there is a risk of not using automatic memory management technology in the iOS App')
        set_values_for_key(key='ARCCHECKRESULT', zh='iOS App程序中存在未使用自动管理内存技术风险',
                           en='There is a risk of not using automatic memory management technology in the iOS App')

        TITLE = get_value('ARCCHECKTITLE')
        LEVEL = 1
        INFO = get_value('ARCCHECKINFO')

        hasBug = True
        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if '_autoreleasePool' in line or '_objc_autorelease' in line or 'autorelease' in line:
                    hasBug = False
                    break
        if hasBug:
            Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result=get_value('ARCCHECKRESULT')).description()


register(ARCCheck)
