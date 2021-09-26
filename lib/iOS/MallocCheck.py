from ..Base import Base
from ..info import Info
from ..ipa import register
from lib.translation import *


class MallocCheck(Base):
    def scan(self):
        set_values_for_key(key='MALLOCCHECKTITLE', zh='内存分配函数不安全风险检测',
                           en='Memory allocation function insecure risk detection')
        set_values_for_key(key='MALLOCCHECKINFO', zh='检测iOS App程序中是否不安全的调用了内存分配函数',
                           en='Detect whether the memory allocation function is unsafely called in the iOS App')
        set_values_for_key(key='MALLOCCHECKRESULT', zh='iOS App程序中不安全的调用了内存分配函数',
                           en='The memory allocation function is unsafely called in the iOS App program')

        TITLE = get_value('MALLOCCHECKTITLE')
        LEVEL = 1
        INFO = get_value('MALLOCCHECKINFO')

        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().lower()
                if '@_malloc' in line:
                    Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result=get_value('MALLOCCHECKRESULT')).description()
                    break


register(MallocCheck)
