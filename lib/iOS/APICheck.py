from ..Base import Base
from ..info import Info
from ..ipa import register
from lib.translation import *


class APICheck(Base):
    def scan(self):
        set_values_for_key(key='APICHECKTITLE', zh='不安全的API函数引用风险检测', en='Unsafe API function reference risk detection')
        set_values_for_key(key='APICHECKINFO', zh='检测iOS App程序中是否引用了不安全的系统API函数',
                           en='Detect whether insecure system API functions are referenced in the iOS App program')

        TITLE = get_value('APICHECKTITLE')
        LEVEL = 2
        INFO = get_value('APICHECKINFO')

        results = []
        blackList = ['@_gets', '@_gets', '@_strcpy', '@_strcat', '@_gets', '@_sprintf', '@_scanf', '@_sscanf',
                     '@_fscanf', '@_vfscanf', '@_vsprintf', '@_vscanf', '@_vsscanf', '@_streadd',
                     '@_strecpy', '@_strtrns', '@_realpath', '@_syslog', '@_getopt', '@_getopt_long', '@_getpass',
                     '@_getchar', '@_fgetc', '@_getc', '@_read', '@_bcopy', '@_fgets', '@_memcpy',
                     '@_snprintf', '@_strccpy', '@_strcadd', '@_strncpy', '@_vsnprintf']
        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().lower()
                if line in blackList and line not in results:
                    results.append(line)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(APICheck)
