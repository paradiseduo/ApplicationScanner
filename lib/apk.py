#!/usr/bin/python3
# -*- coding:utf-8 -*-
import subprocess
import os
import traceback
import shutil
from xml.dom.minidom import parse
import xml.dom.minidom
from lib.info import Info
from lib.tools import randomStr

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
    filePath = inputfile.replace('.apk', '').split('/')[-1] + randomStr(6)
    strline = 'java -jar ./ThirdTools/apktool.jar d -f "' + inputfile + '" -o ' + filePath + ' --only-main-classes'
    subprocess.call(strline, shell=True)
    filePath = os.path.abspath(filePath)
    try:
        appSign(inputfile)
        fingerPrint(filePath)
        permission(filePath)

        for key in scanners.keys():
            c = scanner(key)
            if c:
                c(filePath).scan()
    except:
        print(traceback.format_exc())

    if not save:
        shutil.rmtree(filePath)
    

def appSign(filePath):
    strline = 'java -jar ./ThirdTools/apksigner.jar verify -v --print-certs ' + filePath
    p = subprocess.Popen(strline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    std = p.communicate()
    arr = std[0].decode('utf-8', 'replace').split('\n')
    result = ''
    for line in arr:
        if 'WARNING:' not in line:
            result += line + '\n'
    Info(title='签名信息', level=0, info='签名验证详细信息', result=result).description()


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
    Info(title='证书指纹', level=0, info='证书指纹信息', result=result).description()


def permission(filePath):
    XMLPath = filePath + '/AndroidManifest.xml'
    result = ''
    tree = xml.dom.minidom.parse(XMLPath)
    root = tree.documentElement
    package = root.getAttribute('package')
    result += '  包名: ' + package
    result += '\n  使用权限列表'
    permissionList = root.getElementsByTagName('uses-permission')
    for p in permissionList:
        result += '\n      ' + p.getAttribute('android:name')
    permissionList = root.getElementsByTagName('permission')
    for p in permissionList:
        result += '\n      ' + p.getAttribute('android:name')
    Info(title='权限信息', level=0, info='应用使用权限信息', result=result).description()