from ..Base import Base
from ..info import Info
from ..ipa import register
import json
from lib.translation import *


class SignatureCheck(Base):
    def scan(self):
        set_values_for_key(key='SIGNATURECHECKTITLE', zh='可执行文件被篡改风险检测',
                           en='Potential file tampering vulnerability detection')
        set_values_for_key(key='SIGNATURECHECKINFO', zh='检测ipa包是否存在可执行MachO文件格式被篡改风险',
                           en='Detect whether the ipa package has a risk of tampering with the executable MachO file format')
        set_values_for_key(key='SIGNATURECHECKRESULT', zh='该ipa包可执行MachO文件格式被篡改',
                           en='The ipa package executable MachO file format has been tampered with')

        TITLE = get_value('SIGNATURECHECKTITLE')
        LEVEL = 2
        INFO = get_value('SIGNATURECHECKINFO')

        with open(self.appPath + '/macho.json', 'r') as f:
            dic = json.loads(f.read())
            if dic['signatrue'] != 'LOAD_COMMAND_TYPES.CODE_SIGNATURE':
                Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result=get_value('SIGNATURECHECKRESULT')).description()


register(SignatureCheck)
