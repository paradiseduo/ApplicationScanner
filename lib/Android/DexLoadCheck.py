from lib.translation import *
from ..Base import Base
from ..apk import register
from ..info import Info
from ..tools import *


class DexLoadCheck(Base):
    def scan(self):
        set_values_for_key(key='DEXLOADCHECKTITLE', zh='SDCARD加载dex检测',
                           en='SDCARD loading dex detection')
        set_values_for_key(key='DEXLOADCHECHINFO', zh='检测App程序中的是否存在从sdcard动态加载dex的风险',
                           en='Detect whether there is a risk of dynamically loading dex from sdcard in the App program')

        TITLE = get_value('DEXLOADCHECKTITLE')
        LEVEL = 1
        INFO = get_value('DEXLOADCHECHINFO')

        strline = cmdString(
            f'grep -r "Ldalvik/system/DexClassLoader;-><init>" {self.appPath}'
        )
        paths = getSmalis(os.popen(strline).readlines())
        results = []
        for path in paths:
            with open(path, 'r') as f:
                lines = f.readlines()
                lines.reverse()
                count = len(lines)
                name = getFileName(path)
                for i in range(count):
                    line = lines[i]
                    if 'Ldalvik/system/DexClassLoader;-><init>' in line:
                        start = line.find('{') + 1
                        end = line.find('}')
                        vs = line[start:end]
                        v = vs.split(',')[1].strip()
                        for j in range(i, count):
                            ll = lines[j]
                            llnext = lines[j]
                            if j + 1 < count:
                                llnext = lines[j + 1]
                            if 'Landroid/os/Environment;->getExternalStorageDirectory' in ll and ('.local' in llnext and v in llnext and 'Ljava/lang/String;' in llnext):
                                result = f'{name} : {str(count - i)}'
                                if result not in results:
                                    results.append(result)
                                break
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(DexLoadCheck)
