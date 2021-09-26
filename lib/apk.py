#!/usr/bin/python3
# -*- coding:utf-8 -*-
import traceback
import shutil
from xml.dom.minidom import parse
import xml.dom.minidom
from lib.info import Info
from lib.tools import *
from lib.translation import *

scanners = {}


def register(scanner_class):
    scanners[scanner_class.__name__] = scanner_class


def scanner(scanner_key):
    scanner_class = scanners.get(scanner_key, None)
    if scanner_class is None:
        return None
    return scanner_class


def import_scanners(scanners_imports):
    for runner_import in scanners_imports:
        __import__(runner_import)


from . import Android  # 执行导入包到 scanners


def apkScan(inputfile, save):
    # 解压apk包
    console.print('\n[magenta]Unzip apk [/magenta][bold magenta]' + inputfile + '[/bold magenta]')
    filePath = inputfile.replace('.apk', '').split('/')[-1] + randomStr(6)
    strline = 'java -jar ./ThirdTools/apktool.jar d -f "' + inputfile + '" -o ' + filePath + ' --only-main-classes'
    subprocess.Popen(strline, shell=True).communicate()
    console.print('[bold green]Finish[/bold green]')
    filePath = os.path.abspath(filePath)
    try:
        apkInfo(filePath)
        permissionAndExport(filePath)
        appSign(inputfile)
        fingerPrint(filePath)

        for key in scanners.keys():
            c = scanner(key)
            if c:
                c(filePath).scan()
    except:
        print(traceback.format_exc())

    if not save:
        console.print('\n[bold magenta]Clean cache...[/bold magenta]')
        shutil.rmtree(filePath)
        console.print('[bold green]Finish[/bold green]')
    

def appSign(filePath):
    strline = 'java -jar ./ThirdTools/apksigner.jar verify -v --print-certs ' + filePath
    p = subprocess.Popen(strline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    std = p.communicate()
    arr = std[0].decode('utf-8', 'replace').split('\n')
    result = ''
    for line in arr:
        if 'WARNING:' not in line:
            result += line + '\n'
    set_values_for_key(key='ANDROIDSIGNTITLE', zh='签名信息', en='Signature information')
    set_values_for_key(key='ANDROIDSIGNINFO', zh='签名验证详细信息', en='Signature verification details')
    Info(title=get_value('ANDROIDSIGNTITLE'), level=0, info=get_value('ANDROIDSIGNINFO'), result=result).description()


def fingerPrint(filePath):
    strline = 'cd ' + filePath + '/original/META-INF && (ls | grep *.RSA)'
    out = os.popen(strline).readlines()
    rsa = ''
    for line in out:
        rsa = line[:-1].lstrip()
    strline = 'keytool -printcert -file ' + filePath + '/original/META-INF/' + rsa
    out = os.popen(strline).readlines()
    result = ''
    for line in out:
        result += line
    set_values_for_key(key='ANDROIDCERTTITLE', zh='证书指纹', en='Certificate fingerprint')
    set_values_for_key(key='ANDROIDCERTINFO', zh='证书指纹信息', en='Certificate fingerprint information')
    Info(title=get_value('ANDROIDCERTTITLE'), level=0, info=get_value('ANDROIDCERTINFO'), result=result).description()


def permissionAndExport(filePath):
    set_values_for_key(key='ANDROIDPACKAGENAME', zh='  包名: ', en='  Certificate fingerprint: ')
    set_values_for_key(key='ANDROIDPERMISSIONLIST', zh='\n  使用权限列表', en='\n  Use permission list')

    XMLPath = filePath + '/AndroidManifest.xml'
    result = ''
    tree = xml.dom.minidom.parse(XMLPath)
    root = tree.documentElement
    package = root.getAttribute('package')
    result += get_value('ANDROIDPACKAGENAME') + package
    result += get_value('ANDROIDPERMISSIONLIST')
    permissionList = root.getElementsByTagName('uses-permission')
    for p in permissionList:
        result += '\n      ' + p.getAttribute('android:name')
    permissionList = root.getElementsByTagName('permission')
    for p in permissionList:
        result += '\n      ' + p.getAttribute('android:name')

    set_values_for_key(key='ANDROIDPERMISSIONTITLE', zh='权限信息', en='Permission information')
    set_values_for_key(key='ANDROIDPERMISSIONINFO', zh='应用使用权限信息', en='Application permission information')
    Info(title=get_value('ANDROIDPERMISSIONTITLE'), level=0, info=get_value('ANDROIDPERMISSIONINFO'), result=result).description()
    results = []
    exportedList = root.getElementsByTagName('activity-alias') + root.getElementsByTagName(
        'activity') + root.getElementsByTagName('service') + root.getElementsByTagName(
        'receiver') + root.getElementsByTagName('provider')
    for a in exportedList:
        if a.getAttribute('android:exported') == 'true':
            p = a.getAttribute('android:name')
            results.append(p)

    set_values_for_key(key='ANDROIDEXPORTEDTITLE', zh='组件导出检测', en='Component export detection')
    set_values_for_key(key='ANDROIDEXPORTEDINFO', zh='检测导出的组件信息', en='Detect exported component information')
    Info(title=get_value('ANDROIDEXPORTEDTITLE'), level=0, info=get_value('ANDROIDEXPORTEDINFO'), result="\n".join(results)).description()


def apkInfo(filePath):
    set_values_for_key(key='ANDROIDSDKVERSION', zh='\n  SDK版本: ', en='\n  SDK Version: ')
    set_values_for_key(key='ANDROIDVERSION', zh='\n  版本号: ', en='\n  Version: ')
    set_values_for_key(key='ANDROIDVERSIONNAME', zh='\n  版本名: ', en='\n  Version name: ')

    yml = filePath + '/apktool.yml'
    result = ''
    with open(yml, mode='r') as f:
        io = f.read()
        strArr = str(io).split('\n')
        for s in strArr:
            if 'minSdkVersion' in s:
                result += '  minSdkVersion: ' + s.split(':')[-1].lstrip().replace("'", '')
            if 'targetSdkVersion' in s:
                result += get_value('ANDROIDSDKVERSION') + s.split(':')[-1].lstrip().replace("'", '')
            if 'versionCode' in s:
                result += get_value('ANDROIDVERSION') + s.split(':')[-1].lstrip().replace("'", '')
            if 'versionName' in s:
                result += get_value('ANDROIDVERSIONNAME') + s.split(':')[-1].lstrip().replace("'", '')

    set_values_for_key(key='ANDROIDINFOTITLE', zh='应用基本信息', en='Basic application information')
    set_values_for_key(key='ANDROIDINFOINFO', zh='App的基本信息', en='Basic information of the app')
    Info(title=get_value('ANDROIDINFOTITLE'), level=0, info=get_value('ANDROIDINFOINFO'), result=result).description()
