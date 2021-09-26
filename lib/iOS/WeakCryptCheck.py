from ..Base import Base
from ..info import Info
from ..ipa import register
from lib.translation import *


class WeakCryptCheck(Base):
    def scan(self):
        set_values_for_key(key='WEAKCRYPTCHECKTITLE', zh='AES/DES加密算法不安全使用检测',
                           en='AES/DES encryption algorithm insecure use detection')
        set_values_for_key(key='WEAKCRYPTCHECKINFO', zh='检测iOS App程序中使用AES/DES加密算法时是否使用了不安全的加密模式',
                           en='Detect whether an insecure encryption mode is used when the AES/DES encryption algorithm is used in the iOS App')

        TITLE = get_value('WEAKCRYPTCHECKTITLE')
        LEVEL = 1
        INFO = get_value('WEAKCRYPTCHECKINFO')

        results = []
        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().upper()
                if ('_AES_ECB_ENCRYPT' == line or '_AES_OFB_ENCRYPT' == line or '_DES_ECB_ENCRYPT' == line or '_DES_OFB_ENCRYPT' == line) and line not in results:
                    results.append(line)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(WeakCryptCheck)
