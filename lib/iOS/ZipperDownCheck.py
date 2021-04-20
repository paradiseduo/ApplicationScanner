from ..Base import Base
from ..info import Info
from ..ipa import register

TITLE = 'ZipperDown解压漏洞检测'
LEVEL = 2
INFO = '检测iOS App中是否存在ZipperDown解压漏洞'


class ZipperDownCheck(Base):
    def scan(self):
        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if 'SSZipArchive' in line or 'Ziparchive' in line:
                    Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='iOS App中存在ZipperDown解压漏洞').description()
                    break


register(ZipperDownCheck)
