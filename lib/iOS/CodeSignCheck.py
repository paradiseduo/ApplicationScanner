from ..Base import Base
from ..info import Info
from ..ipa import register
import platform
import subprocess
from lib.translation import *


class CodeSignCheck(Base):
    def scan(self):
        set_values_for_key(key='CODESIGNCHECKTITLE', zh='证书类型检测',
                           en='Certificate type detection')
        set_values_for_key(key='CODESIGNCHECKINFO', zh='检测ipa包的证书类型，是否使用了开发者证书导致无法上架App Store',
                           en='Check the certificate type of the ipa package, whether the developer certificate is used, and the App Store cannot be listed')
        set_values_for_key(key='CODESIGNCHECKRESULT', zh='未使用发布证书打包，无法上架App Store',
                           en='It is not packaged with a release certificate and cannot be put on the App Store')

        TITLE = get_value('CODESIGNCHECKTITLE')
        LEVEL = 1
        INFO = get_value('CODESIGNCHECKINFO')

        hasEXP = True
        if platform.system() == 'Darwin':
            strline = 'codesign -vv -d ' + self.appBinPath
            p = subprocess.Popen(strline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out = p.communicate()[1].decode('utf-8', 'ignore')
            arr = out.split('\n')
            for line in arr:
                if line.startswith('Authority=') and line.endswith(')'):
                    result = line.split('=')[-1]
                    if 'Apple Distribution' in result:
                        hasEXP = False
        else:
            with open(self.appPath+'/ClassDump', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if 'Apple Distribution' in line:
                        hasEXP = False
        if hasEXP:
            Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result=get_value('CODESIGNCHECKRESULT')).description()


register(CodeSignCheck)
