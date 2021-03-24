from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *

TITLE = 'WebView安全检测'
LEVEL = 1
INFO = '检测App程序WebView是否存在风险'


class WebViewCheck(Base):
    def scan(self):
        strline = cmdString(
            'grep -r "Landroid/webkit/WebView" ' + self.appPath)
        paths = getSmalis(os.popen(strline).readlines())
        resultsPassword = []
        resultsCert = []
        resultsRCE = []
        resultsDebug = []
        resultsHidden = []
        for path in paths:
            with open(path, 'r') as f:
                lines = f.readlines()
                count = len(lines)
                name = getFileName(path)
                hasExp = True
                vvv = 3
                for i in range(0, count):
                    line = lines[i]
                    # 证书校验
                    if 'Landroid/webkit/SslErrorHandler;->proceed()V' in line:
                        result = name + ' : ' + str(i + 1)
                        if result not in resultsCert:
                            resultsCert.append(result)
                    # 代码执行
                    if 'Landroid/webkit/WebView;->addJavascriptInterface' in line:
                        result = name + ' : ' + str(i + 1)
                        if result not in resultsRCE:
                            resultsRCE.append(result)
                lines.reverse()
                for i in range(0, count):
                    line = lines[i]
                    # Debug检测
                    if 'Landroid/webkit/WebView;->setWebContentsDebuggingEnabled(Z)V' in line:
                        start = line.find("{") + 1
                        end = line.find("}")
                        v = line[start:end]
                        for j in range(i, count):
                            ll = lines[j]
                            if v in ll and '0x1' in ll and 'const' in ll:
                                result = name + ' : ' + str(count - i)
                                if result not in resultsDebug:
                                    resultsDebug.append(result)
                                break
                    # 隐藏接口
                    if 'Landroid/webkit/WebView;->removeJavascriptInterface' in line:
                        start = line.find("{") + 1
                        end = line.find("}")
                        v = line[start:end].split(', ')[-1]
                        for j in range(i, count):
                            if vvv == 0:
                                break
                            ll = lines[j]
                            if v in ll:
                                if 'searchBoxJavaBridge_' in ll:
                                    vvv -= 1
                                if 'accessibility' in ll:
                                    vvv -= 1
                                if 'accessibilityTraversal' in ll:
                                    vvv -= 1
                        if vvv > 0 and name not in resultsHidden:
                            resultsHidden.append(name)
                    # 明文密码
                    if 'Landroid/webkit/WebSettings;->setSavePassword' in line:
                        start = line.find("{") + 1
                        end = line.find("}")
                        v = line[start:end].split(', ')[-1]
                        for j in range(i, count):
                            ll = lines[j]
                            if v in ll and 'const' in ll and '0x0' in ll:
                                hasExp = False
                                break
                        result = name + ' : ' + str(count - i)
                        if hasExp and result not in resultsPassword:
                            resultsPassword.append(result)
        Info(key=self.__class__, title='WebView明文存储密码检测', level=1, info='检测App程序是否存在WebView明文存储密码风险',
             result='\n'.join(resultsPassword)).description()
        Info(key=self.__class__, title='Webview绕过证书校验漏洞', level=1, info='检测App应用的Webview组件是否在发现https网页证书错误后继续加载页面',
             result='\n'.join(resultsCert)).description()
        Info(key=self.__class__, title='WebView远程代码执行检测', level=3, info='检测App应用的Webview组件中是否存在远程代码执行漏洞',
             result='\n'.join(resultsRCE)).description()
        Info(key=self.__class__, title='WebView远程调试检测', level=2, info='检测App程序是否存在Webview远程调试风险',
             result='\n'.join(resultsDebug)).description()
        Info(key=self.__class__, title='WebView未移除有风险的系统隐藏接口漏洞', level=2, info='检测App程序中是否存在未移除的Webview系统隐藏接口',
             result='\n'.join(resultsHidden)).description()


register(WebViewCheck)
