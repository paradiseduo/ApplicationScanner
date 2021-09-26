import xml.dom.minidom
from ..Base import Base
from ..info import Info
from ..apk import register
import os
from lib.translation import *


class BackupCheck(Base):
    def scan(self):
        set_values_for_key(key='BACKUPCHECKTITLE', zh='应用数据任意备份风险检测', en='Application data arbitrary backup risk detection')
        set_values_for_key(key='BACKUPCHECHINFO', zh='检测App是否存在应用数据被任意备份的风险', en='Detect whether the app has the risk of app data being arbitrarily backed up')

        TITLE = get_value('BACKUPCHECKTITLE')
        LEVEL = 2
        INFO = get_value('BACKUPCHECHINFO')

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