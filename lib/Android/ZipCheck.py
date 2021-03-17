from ..Base import Base
from ..info import Info
from ..tools import *
from ..apk import register

TITLE = 'Zip文件解压目录遍历检测'
LEVEL = 3
INFO = '检测Apk中是否存在Zip文件解压目录遍历漏洞'


class ZipCheck(Base):
    def scan(self):
        strline = cmdString('grep -r "Ljava/util/zip/ZipInputStream" ' + self.appPath)
        arr = os.popen(strline).readlines()
        results = []
        for item in arr:
            if '.smali:' in item:
                path = item.split(':')[0]
                with open(path, 'r') as f:
                    lines = f.readlines()
                    count = len(lines)
                    index = 0
                    name = getFileName(path)
                    for line in lines:
                        index += 1
                        isExp = True
                        if 'Ljava/util/zip/ZipEntry;->getName()Ljava/lang/String' in line:
                            for i in range(index, count):
                                p = lines[i]
                                if '../' in p and 'const-string' in p:
                                    isExp = False
                                if '.end method' in p:
                                    if isExp:
                                        result = name + ' : ' + str(index)
                                        if result not in results:
                                            results.append(result)
                                    break
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(ZipCheck)