from ..Base import Base
from ..info import Info
from ..ipa import register
import json

TITLE = '地址空间随机化技术检测'
LEVEL = 1
INFO = '检测iOS App程序中是否存在未使用地址空间随机化技术风险'


class ASLRCheck(Base):
    def scan(self):
        with open(self.appPath + '/macho.json', 'r') as f:
            try:
                dic = json.loads(f.read())
                if not dic['has_pie']:
                    Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO,
                         result='该App程序中未使用地址空间随机化技术').description()
                return
            except:
                return


register(ASLRCheck)
