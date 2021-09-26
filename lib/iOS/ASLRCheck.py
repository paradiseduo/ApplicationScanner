from ..Base import Base
from ..info import Info
from ..ipa import register
import json
from lib.translation import *


class ASLRCheck(Base):
    def scan(self):
        set_values_for_key(key='ASLRCHECKTITLE', zh='地址空间随机化技术检测',
                           en='Address space randomization technology detection')
        set_values_for_key(key='ASLRCHECKINFO', zh='检测iOS App程序中是否存在未使用自动管理内存技术风险',
                           en='Detect whether there is an unused address space randomization technology risk in the iOS App')
        set_values_for_key(key='ASLRCHECKRESULT', zh='iOS App程序中存在未使用自动管理内存技术风险',
                           en='The address space randomization technology is not used in the App program')

        TITLE = get_value('ASLRCHECKTITLE')
        LEVEL = 1
        INFO = get_value('ASLRCHECKINFO')

        with open(self.appPath + '/macho.json', 'r') as f:
            try:
                dic = json.loads(f.read())
                if not dic['has_pie']:
                    Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO,
                         result=get_value('ASLRCHECKRESULT')).description()
                return
            except:
                return


register(ASLRCheck)
