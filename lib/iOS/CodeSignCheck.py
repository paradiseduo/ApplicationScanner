from ..Base import Base
from ..info import Info
from ..ipa import register
import platform
import subprocess

TITLE = '证书类型检测'
LEVEL = 1
INFO = '检测ipa包的证书类型，是否使用了开发者证书导致无法上架App Store'


class CodeSignCheck(Base):
    def scan(self):
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
            Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='未使用发布证书打包，无法上架App Store').description()


register(CodeSignCheck)
