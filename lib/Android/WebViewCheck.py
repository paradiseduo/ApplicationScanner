from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *
from lib.translation import *


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

        set_values_for_key(key='WEBPASSWORDCHECKTITLE', zh='WebView明文存储密码检测',
                           en='WebView plaintext storage password detection')
        set_values_for_key(key='WEBPASSWORDCHECHINFO', zh='检测App程序是否存在WebView明文存储密码风险',
                           en="Detect whether the App program has the risk of WebView storing passwords in plain text")
        Info(key=self.__class__, title=get_value('WEBPASSWORDCHECKTITLE'), level=1, info=get_value('WEBPASSWORDCHECHINFO'),
             result='\n'.join(resultsPassword)).description()

        set_values_for_key(key='WEBCERTCHECKTITLE', zh='Webview绕过证书校验漏洞',
                           en='Webview bypasses certificate verification vulnerability')
        set_values_for_key(key='WEBCERTCHECHINFO', zh='检测App应用的Webview组件是否在发现https网页证书错误后继续加载页面',
                           en="Check whether the Webview component of the App application continues to load the page after finding the https webpage certificate error")
        Info(key=self.__class__, title=get_value('WEBCERTCHECKTITLE'), level=1, info=get_value('WEBCERTCHECHINFO'),
             result='\n'.join(resultsCert)).description()

        set_values_for_key(key='WEBRCECHECKTITLE', zh='WebView远程代码执行检测',
                           en='WebView remote code execution detection')
        set_values_for_key(key='WEBRCECHECHINFO', zh='检测App应用的Webview组件中是否存在远程代码执行漏洞',
                           en="Detect whether there is a remote code execution vulnerability in the Webview component of the App application")
        Info(key=self.__class__, title=get_value('WEBRCECHECKTITLE'), level=3, info=get_value('WEBRCECHECHINFO'),
             result='\n'.join(resultsRCE)).description()

        set_values_for_key(key='WEBDEBUGCHECKTITLE', zh='WebView远程调试检测',
                           en='WebView remote debugging detection')
        set_values_for_key(key='WEBDEBUGCHECHINFO', zh='检测App程序是否存在Webview远程调试风险',
                           en="Detect whether there is a risk of Webview remote debugging in the App program")
        Info(key=self.__class__, title=get_value('WEBDEBUGCHECKTITLE'), level=2, info=get_value('WEBDEBUGCHECHINFO'),
             result='\n'.join(resultsDebug)).description()

        set_values_for_key(key='WEBREMOVECHECKTITLE', zh='WebView未移除有风险的系统隐藏接口漏洞',
                           en='WebView did not remove the risky system hidden interface vulnerabilities')
        set_values_for_key(key='WEBREMOVECHECHINFO', zh='检测App程序中是否存在未移除的Webview系统隐藏接口',
                           en="Check whether there is an unremoved hidden interface of the Webview system in the App program")
        Info(key=self.__class__, title=get_value('WEBREMOVECHECKTITLE'), level=2, info=get_value('WEBREMOVECHECHINFO'),
             result='\n'.join(resultsHidden)).description()


register(WebViewCheck)
