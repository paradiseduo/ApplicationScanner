import xml.dom.minidom
from ..Base import Base
from ..info import Info
from ..apk import register
import os

TITLE = '应用数据任意备份风险检测'
LEVEL = 2
INFO = '检测App是否存在应用数据被任意备份的风险'


class BackupCheck(Base):
    def scan(self):
        strline = 'find ' + self.appPath +' -name AndroidManifest.xml | grep -v "/original/"'
        arr = os.popen(strline).readlines()
        for item in arr:
            tree = xml.dom.minidom.parse(item[:-1])
            root = tree.documentElement
            application = root.getElementsByTagName('application')
            result = ''
            for a in application:
                if a.getAttribute('android:allowBackup') == 'true':
                    result = 'android:allowBackup = true'
            Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result=result).description()


register(BackupCheck)