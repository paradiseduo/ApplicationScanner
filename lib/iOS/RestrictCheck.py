from ..Base import Base
from ..info import Info
from ..ipa import register
import json
from lib.translation import *


class RestrictCheck(Base):
    def scan(self):
        set_values_for_key(key='RESTRICTCHECKTITLE', zh='注入攻击风险检测',
                           en='Injection attack risk detection')
        set_values_for_key(key='RESTRICTCHECKINFO', zh='检测ipa包是否存在dyld注入攻击风险',
                           en='Check whether there is a risk of dyld injection attack in the ipa package')
        set_values_for_key(key='RESTRICTCHECKRESULT', zh='该App程序存在dyld注入风险',
                           en='The App program has a risk of dyld injection')

        TITLE = get_value('RESTRICTCHECKTITLE')
        LEVEL = 2
        INFO = get_value('RESTRICTCHECKINFO')

        with open(self.appPath + '/macho.json', 'r') as f:
            dic = json.loads(f.read())
            if not dic['has_restrict']:
                Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result=get_value('RESTRICTCHECKRESULT')).description()


register(RestrictCheck)
