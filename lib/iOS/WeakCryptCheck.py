from ..Base import Base
from ..info import Info
from ..ipa import register

TITLE = 'AES/DES加密算法不安全使用检测'
LEVEL = 1
INFO = '检测iOS App程序中使用AES/DES加密算法时是否使用了不安全的加密模式'


class WeakCryptCheck(Base):
    def scan(self):
        results = []
        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().upper()
                if ('_AES_ECB_ENCRYPT' == line or '_AES_OFB_ENCRYPT' == line or '_DES_ECB_ENCRYPT' == line or '_DES_OFB_ENCRYPT' == line) and line not in results:
                    results.append(line)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(WeakCryptCheck)
