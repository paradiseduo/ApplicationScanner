from ..Base import Base
from ..info import Info
from ..ipa import register

TITLE = 'Webview组件跨域访问风险检测'
LEVEL = 3
INFO = '检测iOS App程序中是否可利用Webview组件跨域访问读取或修改文件的风险'


class WebViewCheck(Base):
    def scan(self):
        results = []
        with open(self.appPath + '/ClassDump', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'allowFileAccessFromFileURLs' in line or 'allowUniversalAccessFromFileURLsActivity' in line:
                    results.append(line.strip())
            Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()



register(WebViewCheck)
