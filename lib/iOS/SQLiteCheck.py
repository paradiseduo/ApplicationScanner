from ..Base import Base
from ..info import Info
from ..ipa import register

TITLE = 'SQLite内存破坏漏洞检测'
LEVEL = 2
INFO = '检测iOS App程序中是否存在SQLite内存破坏漏洞'


class SQLiteCheck(Base):
    def scan(self):
        with open(self.appPath + '/StringDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().lower()
                if 'fts3_tokenizer' in line:
                    Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='iOS App程序中存在SQLite内存破坏漏洞').description()
                    break


register(SQLiteCheck)
