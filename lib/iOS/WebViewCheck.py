from ..Base import Base
from ..info import Info
from ..ipa import register
from lib.translation import *


class WebViewCheck(Base):
    def scan(self):
        set_values_for_key(key='IOSWEBVIEWCHECKTITLE', zh='Webview组件跨域访问风险检测',
                           en='Webview component cross-domain access risk detection')
        set_values_for_key(key='IOSWEBVIEWCHECKINFO', zh='检测iOS App程序中是否可利用Webview组件跨域访问读取或修改文件的风险',
                           en='Detect whether the Webview component can be used in the iOS App program to access the risk of reading or modifying files across domains')

        TITLE = get_value('IOSWEBVIEWCHECKTITLE')
        LEVEL = 3
        INFO = get_value('IOSWEBVIEWCHECKINFO')

        results = []
        with open(self.appPath + '/ClassDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'allowFileAccessFromFileURLs' in line or 'allowUniversalAccessFromFileURLsActivity' in line:
                    results.append(line.strip())
            Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()



register(WebViewCheck)
