import os
from ..Base import Base
from ..info import Info
from ..apk import register

TITLE = 'So文件破解风险检测'
LEVEL = 2
INFO = '检测Apk中的so文件是否可被破解读取'


class SoCheck(Base):
    def scan(self):
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