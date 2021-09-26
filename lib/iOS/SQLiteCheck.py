from ..Base import Base
from ..info import Info
from ..ipa import register
from lib.translation import *


class SQLiteCheck(Base):
    def scan(self):
        set_values_for_key(key='SQLLITECHECKTITLE', zh='SQLite内存破坏漏洞检测',
                           en='SQLite memory corruption vulnerability detection')
        set_values_for_key(key='SQLLITECHECKINFO', zh='检测iOS App程序中是否存在SQLite内存破坏漏洞',
                           en='Detect whether there is a SQLite memory corruption vulnerability in the iOS App')
        set_values_for_key(key='SQLLITECHECKRESULT', zh='iOS App程序中存在SQLite内存破坏漏洞',
                           en='SQLite memory corruption vulnerability exists in iOS App')

        TITLE = get_value('SQLLITECHECKTITLE')
        LEVEL = 2
        INFO = get_value('SQLLITECHECKINFO')

        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().lower()
                if 'fts3_tokenizer' in line:
                    Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result=get_value('SQLLITECHECKRESULT')).description()
                    break


register(SQLiteCheck)
