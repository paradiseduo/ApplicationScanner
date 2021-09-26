from ..Base import Base
from ..info import Info
from ..ipa import register
from lib.translation import *


class ZipperDownCheck(Base):
    def scan(self):
        set_values_for_key(key='ZIPPERDOWNCHECKTITLE', zh='ZipperDown解压漏洞检测',
                           en='ZipperDown decompression vulnerability detection')
        set_values_for_key(key='ZIPPERDOWNCHECKINFO', zh='检测iOS App中是否存在ZipperDown解压漏洞',
                           en='Check whether there is a ZipperDown decompression vulnerability in the iOS App')
        set_values_for_key(key='ZIPPERDOWNCHECKRESULT', zh='iOS App中存在ZipperDown解压漏洞',
                           en='There is a ZipperDown decompression vulnerability in the iOS App')

        TITLE = get_value('ZIPPERDOWNCHECKTITLE')
        LEVEL = 2
        INFO = get_value('ZIPPERDOWNCHECKINFO')

        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if 'SSZipArchive' in line or 'Ziparchive' in line:
                    Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result=get_value('ZIPPERDOWNCHECKRESULT')).description()
                    break


register(ZipperDownCheck)
