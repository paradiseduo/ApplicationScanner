from ..Base import Base
from ..info import Info
from ..ipa import register
import json

TITLE = '可执行文件被篡改风险检测'
LEVEL = 2
INFO = '检测ipa包是否存在可执行MachO文件格式被篡改风险'


class SignatureCheck(Base):
    def scan(self):
        with open(self.appPath + '/macho.json', 'r') as f:
            dic = json.loads(f.read())
            if dic['signatrue'] != 'LOAD_COMMAND_TYPES.CODE_SIGNATURE':
                Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='该ipa包可执行MachO文件格式被篡改').description()


register(SignatureCheck)
