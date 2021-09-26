from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *
from lib.translation import *


class EncryptCheck(Base):
    def scan(self):
        set_values_for_key(key='ENCRYPTCHECKTITLE', zh='AES/DES弱加密风险检测',
                           en='AES/DES weak encryption risk detection')
        set_values_for_key(key='ENCRYPTCHECHINFO', zh='检测App中是否存在AES/DES弱加密风险',
                           en='Detect whether there is a risk of weak AES/DES encryption in the App')

        TITLE = get_value('ENCRYPTCHECKTITLE')
        LEVEL = 1
        INFO = get_value('ENCRYPTCHECHINFO')

        strline = cmdString(
            'grep -r "Ljavax/crypto/Cipher;->getInstance(Ljava/lang/String;)Ljavax/crypto/Cipher;" ' + self.appPath)
        paths = getSmalis(os.popen(strline).readlines())
        results = []
        for path in paths:
            with open(path, 'r') as f:
                lines = f.readlines()
                lines.reverse()
                count = len(lines)
                name = getFileName(path)
                for i in range(0, count):
                    line = lines[i]
                    if 'Ljavax/crypto/Cipher;->getInstance(Ljava/lang/String;)Ljavax/crypto/Cipher;' in line:
                        start = line.find('{') + 1
                        end = line.find('}')
                        v = line[start:end]
                        for j in range(i, count):
                            ll = lines[j]
                            if 'const-string ' + v in ll:
                                s = ll.strip().split(', ')[-1].replace('"', '')
                                if 'ECB' in s or 'DES' == s or 'AES' == s:
                                    result = name + ' : ' + str(count - i)
                                    if result not in results:
                                        results.append(result)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(EncryptCheck)
