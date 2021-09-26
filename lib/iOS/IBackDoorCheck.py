from ..Base import Base
from ..info import Info
from ..ipa import register
from lib.translation import *


class IBackDoorCheck(Base):
    def scan(self):
        set_values_for_key(key='IBACKDOORCHECKTITLE', zh='iBackDoor控制漏洞检测',
                           en='iBackDoor control vulnerability detection')
        set_values_for_key(key='IBACKDOORCHECKINFO', zh='检测iOS App中是否存在可被远程控制的iBackDoor漏洞',
                           en='Detect whether there is an iBackDoor vulnerability that can be remotely controlled in the iOS App')
        set_values_for_key(key='IBACKDOORCHECKRESULT', zh='iOS App中存在可被远程控制的iBackDoor漏洞',
                           en='There is an iBackDoor vulnerability in the iOS App that can be remotely controlled')

        TITLE = get_value('IBACKDOORCHECKTITLE')
        LEVEL = 3
        INFO = get_value('IBACKDOORCHECKINFO')

        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if 'mobiSage' in line:
                    Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result=get_value('IBACKDOORCHECKRESULT')).description()
                    break


register(IBackDoorCheck)
