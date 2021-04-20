from ..Base import Base
from ..info import Info
from ..ipa import register
import json

TITLE = '注入攻击风险检测'
LEVEL = 2
INFO = '检测ipa包是否存在dyld注入攻击风险'


class RestrictCheck(Base):
    def scan(self):
        with open(self.appPath + '/macho.json', 'r') as f:
            dic = json.loads(f.read())
            if not dic['has_restrict']:
                Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='该App程序存在dyld注入风险').description()


register(RestrictCheck)
