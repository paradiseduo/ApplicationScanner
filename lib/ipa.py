#!/usr/bin/python3
# -*- coding:utf-8 -*-
import shutil
import termcolor
import os
import subprocess
import lief
import json
import platform
from lib.tools import *
from lib.info import Info

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


from . import iOS  # 执行导入包到 scanners


def ipaScan(filePath, save):
    # 解压ipa文件
    termcolor.cprint('Unzip ' + filePath, 'white')
    filePath, appName = ipatool(filePath)
    appBinName = appName.replace('.app', '')
    appBinPath = filePath + '/' + appName + '/' + appBinName
    appInfoPath = filePath + '/' + appName + '/' + 'Info.plist'
    termcolor.cprint('Finish', 'green')
    try:
        termcolor.cprint('ClassDump ' + appBinPath, 'white')
        classDump(filePath, appBinPath)
        termcolor.cprint('Finish', 'green')
        iOSAuthority(appInfoPath)
        iOSRpath(appBinPath)
        # files = getIPAFiles(filePath)
        # for file in files:
        for key in scanners.keys():
            c = scanner(key)
            if c:
                c(filePath).scan()
    except:
        import traceback
        print(traceback.format_exc())
    if not save:
        shutil.rmtree(filePath)


def ipatool(inputfile):
    appName = ''
    filePath = 'Payload' + randomStr(6)
    strline = 'cp "' + inputfile + '" test.zip && unzip -o test.zip'
    subprocess.call(strline, shell=True, stdout=subprocess.DEVNULL)
    subprocess.call('rm -rf test.zip', shell=True, stdout=subprocess.DEVNULL)
    subprocess.call('mv Payload ' + filePath, shell=True, stdout=subprocess.DEVNULL)
    p = subprocess.Popen('cd ' + filePath + ' && ls', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    arr = p.communicate()[0].decode('utf-8', 'replace').split('\n')
    for item in arr:
        if '.app' in item:
            # 获取APP名称
            appName = item
            break
    return filePath, appName


def getIPAFiles(dir):
    filesArray = []
    dirlist = os.walk(dir)
    for root, dirs, files in dirlist:
        for file in files:
            if file.endswith('.nib') \
                    or file.endswith('.png') \
                    or file.endswith('.jpg') \
                    or file.endswith('.gif') \
                    or file.endswith('.svga') \
                    or file.endswith('.dylib') \
                    or file.endswith('.strings') \
                    or file.endswith('.mp3') \
                    or file.endswith('.zip') \
                    or file.endswith('.ttf'):
                continue
            else:
                filesArray.append(os.path.join(root, file))
    return filesArray


def classDump(filePath, appBinPath):
    strline = 'strings -a ' + appBinPath + " > " + os.path.abspath(filePath) + '/StringDump'
    subprocess.Popen(strline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    strline = 'strings -a ' + appBinPath + " | grep ']$' | grep '^-\[\|^+\[' > " + os.path.abspath(filePath) + '/ClassDump'
    subprocess.Popen(strline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    strline = 'strings -a ' + appBinPath + " | grep '^http://\|^https://' > " + os.path.abspath(filePath) + '/URLDump'
    subprocess.Popen(strline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    strline = 'strings -a ' + appBinPath + " | grep '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)' > " + os.path.abspath(filePath) + '/IPDump'
    subprocess.Popen(strline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    iOSMachO(appBinPath, filePath)


def iOSMachO(appBinPath, filePath):
    macho = lief.MachO.parse(appBinPath, config=lief.MachO.ParserConfig.quick)
    macho = macho.at(0)

    stk_check = '___stack_chk_fail'
    stk_guard = '___stack_chk_guard'
    ipt_list = set()
    for ipt in macho.imported_functions:
        ipt_list.add(str(ipt))
    has_canary = stk_check in ipt_list and stk_guard in ipt_list

    has_arc = False
    for func in macho.imported_functions:
        if str(func).strip() == '_objc_release':
            has_arc = True
            break

    has_restrict = False
    for segment in macho.segments:
        if segment.name.lower() == '__restrict':
            has_restrict = True
            break

    signatrue = ''
    for item in macho.commands:
        signatrue = str(item.command)

    dic = {
        'name': macho.name,
        'has_nx': macho.has_nx,
        'has_pie': macho.is_pie,
        'has_rpath': macho.has_rpath,
        'crypt_id': macho.encryption_info.crypt_id,
        'has_canary': has_canary,
        'has_arc': has_arc,
        'has_restrict': has_restrict,
        'signatrue': signatrue
    }

    with open(filePath+'/macho.json', mode='w') as f:
        json.dump(dic, f)


def iOSRpath(binPath):
    results = []
    p = subprocess.Popen('strings -a ' + binPath + '| grep @rpath | grep -v libswift', shell=True, stdout=subprocess.PIPE)
    aa = p.communicate()[0].decode('utf-8', 'ignore')
    arr = aa.split('\n')
    for line in arr:
        if len(line) > 1 and line not in results:
            framework = line.split('/')[1]
            results.append(framework)
    Info(key='Info', title='三方库列表', level=0, info='查看应用使用的所有三方库', result="\n".join(results)).description()


def iOSAuthority(filePath):
    results = []
    if platform.system() == 'Linux':
        if 'Debian' in platform.uname().version:
            strline = "plistutil -i " + filePath + " -f xml"
        elif 'centos' in platform.uname().version:
            strline = "plistutil -i " + filePath
        p = subprocess.Popen(strline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = p.communicate()[0].decode('utf-8', 'ignore')
        arr = out.split('\n')
        for i in range(0, len(arr)):
            item = arr[i]
            if 'UsageDescription' in item:
                item = item.replace('<key>', '').replace('</key>', '')
                itemNext = arr[i+1].replace('<string>', '').replace('</string>', '')
                results.append(item + ":" + itemNext)
    elif platform.system() == 'Darwin':
        strline = "/usr/libexec/PlistBuddy -c 'Print' " + filePath
        p = subprocess.Popen(strline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = p.communicate()[0].decode('utf-8', 'ignore')
        arr = out.split('\n')
        for item in arr:
            if 'Description' in item:
                ar = item.split('=')
                results.append(ar[0].strip() + ':' + ar[1].strip())
    Info(key='Info', title='应用权限列表', level=0, info='查看应用使用的所有权限', result="\n".join(results)).description()