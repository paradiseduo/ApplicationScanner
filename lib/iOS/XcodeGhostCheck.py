from ..Base import Base
from ..info import Info
from ..ipa import register
from lib.translation import *


class XcodeGhostCheck(Base):
    def scan(self):
        set_values_for_key(key='XCODECHECKTITLE', zh='XcodeGhost感染检测',
                           en='XcodeGhost infection detection')
        set_values_for_key(key='XCODECHECKINFO', zh='检测iOS App中是否被植入XcodeGhost恶意代码',
                           en='Detect whether XcodeGhost malicious code is implanted in the iOS App')
        set_values_for_key(key='XCODECHECKRESULT', zh='iOS App中被植入XcodeGhost恶意代码',
                           en='XcodeGhost malicious code implanted in iOS App')

        TITLE = get_value('XCODECHECKTITLE')
        LEVEL = 3
        INFO = get_value('XCODECHECKINFO')

        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().upper()
                if 'init.icloud-analysis.com' in line:
                    Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result=get_value('XCODECHECKRESULT')).description()
                    break


register(XcodeGhostCheck)
