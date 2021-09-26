from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *
from lib.translation import *


class ScreenshotCheck(Base):
    def scan(self):
        set_values_for_key(key='SCREENCHECKTITLE', zh='截屏攻击风险检测',
                           en='Screen capture attack risk detection')
        set_values_for_key(key='SCREENCHECHINFO', zh='检测App是否存在截屏攻击风险检测',
                           en="Detect whether the app has a screenshot attack risk detection")

        TITLE = get_value('SCREENCHECKTITLE')
        LEVEL = 1
        INFO = get_value('SCREENCHECHINFO')

        strline = cmdString('grep -r ".super Landroid/app/Activity;" ' + self.appPath)
        paths = getSmalis(os.popen(strline).readlines())
        results = []
        for path in paths:
            hasEXP = True
            with open(path, 'r') as f:
                lines = f.readlines()
                lines.reverse()
                count = len(lines)
                name = getFileName(path)
                for i in range(0, count):
                    if not hasEXP:
                        break
                    line = lines[i]
                    if 'Landroid/view/Window;->setFlags' in line or 'Landroid/view/Window;->addFlags' in line:
                        varr = line.strip().split(',')
                        v = 'paradiseduo'
                        if len(varr) > 3:
                            v1 = varr[1].strip()
                            v2 = varr[2].strip().replace('}', '')
                            if v1 == v2:
                                v = v1
                        else:
                            v = varr[1].strip().replace('}', '')
                        for j in range(i, count):
                            if v in line and '0x2000' in lines[j]:
                                hasEXP = False
                                break
                        if name not in results:
                            results.append(name)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(ScreenshotCheck)