from ..Base import Base
from ..info import Info
from ..tools import *
from ..apk import register
from lib.translation import *


class ZipCheck(Base):
    def scan(self):
        set_values_for_key(key='ZIPCHECKTITLE', zh='Zip文件解压目录遍历检测',
                           en="Zip file decompression directory traversal detection")
        set_values_for_key(key='ZIPDCHECHINFO', zh='检测Apk中是否存在Zip文件解压目录遍历漏洞',
                           en="Detect whether there is a traversal vulnerability in Zip file decompression directory in Apk")

        TITLE = get_value('ZIPCHECKTITLE')
        LEVEL = 3
        INFO = get_value('ZIPDCHECHINFO')

        strline = cmdString('grep -r "Ljava/util/zip/ZipInputStream" ' + self.appPath)
        paths = getSmalis(os.popen(strline).readlines())
        results = []
        for path in paths:
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