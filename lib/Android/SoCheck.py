import os
from ..Base import Base
from ..info import Info
from ..apk import register
from lib.translation import *


class SoCheck(Base):
    def scan(self):
        set_values_for_key(key='SOCHECKTITLE', zh='So文件破解风险检测',
                           en='So file cracking risk detection')
        set_values_for_key(key='SOCHECHINFO', zh='检测Apk中的so文件是否可被破解读取',
                           en="Detect whether the so file in Apk can be cracked and read")

        TITLE = get_value('SOCHECKTITLE')
        LEVEL = 2
        INFO = get_value('SOCHECHINFO')

        strline = 'find ' + self.appPath + ' -name *.so | grep -v "/original/"'
        arr = os.popen(strline).readlines()
        result = ''
        for item in arr:
            strline = 'readelf -S ' + item[:-1]
            out = os.popen(strline).readlines()
            if 'section in the dynamic segment' not in out:
                filePath = '/'.join(item[:-1].split('/')[-2:])
                result += filePath + '\n'
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result=result).description()


register(SoCheck)