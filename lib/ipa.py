#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os.path
import plistlib
import shutil
import lief
import json
import platform
from lib.tools import *
from lib.info import Info
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


from . import iOS  # 执行导入包到 scanners


def ipaScan(filePath, save):
    # 解压ipa文件
    console.print('\n[magenta]Unzip ipa [/magenta][bold magenta]' + filePath + '[/bold magenta]')
    filePath, appName = ipatool(filePath)
    appBinName = appName.replace('.app', '')
    appPath = f'{filePath}/{appName}'
    appBinPath = f'{appPath}/{appBinName}'
    if not os.path.exists(appBinPath):
        for parent, dirnames, filenames in os.walk(appPath, followlinks=False):
            if parent == appPath:
                for filename in filenames:
                    if '.' not in filename:
                        newPath = os.path.join(parent, filename)
                        arr = RunCMD(f'file \'{newPath}\'').execute()[0].decode('utf-8', 'replace').split('\n')
                        for item in arr:
                            if 'Mach-O' in item:
                                appBinPath = newPath
                                break
    appInfoPath = f'{filePath}/{appName}/Info.plist'
    console.print('[bold green]Finish[/bold green]')
    try:
        iOSInfo(appInfoPath)
        iOSAuthority(appInfoPath)
        console.print('[magenta]Reverse [/magenta][bold magenta]' + appBinPath + '[/bold magenta]')
        reverse(filePath, appBinPath)
        console.print('[bold green]Finish[/bold green]')
        iOSMachO(appBinPath, filePath)
        iOSRpath(filePath + '/RpathDump')
        iOSCert(appInfoPath, filePath, appBinPath)
        for key in scanners.keys():
            c = scanner(key)
            if c:
                c(filePath, appBinPath).scan()
    except:
        import traceback
        print(traceback.format_exc())
    if not save:
        console.print('\n[bold magenta]Clean cache...[/bold magenta]')
        shutil.rmtree(filePath)
        console.print('[bold green]Finish[/bold green]')


def ipatool(inputfile):
    appName = ''
    filePath = f'Payload{randomStr(6)}'
    RunCMD(f'unzip -o \'{inputfile}\' -d .').execute()
    RunCMD(f'mv Payload \'{filePath}\'').execute()
    arr = RunCMD(f'cd \'{filePath}\' && ls').execute()[0].decode('utf-8', 'replace').split('\n')
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


def iOSInfo(appInfoPath):
    results = []
    with open(appInfoPath, 'rb') as fp:
        pl = plistlib.load(fp)

    set_values_for_key(key='CFBundleDisplayName', zh='App名称: ', en='Application Name: ')
    set_values_for_key(key='CFBundleIdentifier', zh='Bundle Identifier: ', en='Bundle Identifier: ')
    set_values_for_key(key='CFBundleShortVersionString', zh='包版本: ', en='Package Version: ')
    set_values_for_key(key='CFBundleVersion', zh='编译版本: ', en='Build Version: ')
    set_values_for_key(key='DTSDKName', zh='SDK版本: ', en='SDK version: ')
    set_values_for_key(key='MinimumOSVersion', zh='最低系统版本: ', en='Minimum system version: ')

    results.append(get_value('CFBundleDisplayName') + pl['CFBundleDisplayName'])
    results.append(get_value('CFBundleIdentifier') + pl['CFBundleIdentifier'])
    results.append(get_value('CFBundleShortVersionString') + pl['CFBundleShortVersionString'])
    results.append(get_value('CFBundleVersion') + pl['CFBundleVersion'])
    results.append(get_value('DTSDKName') + pl['DTSDKName'])
    results.append(get_value('MinimumOSVersion') + pl['MinimumOSVersion'])

    set_values_for_key(key='BaseTitle', zh='APP基本信息', en='Application essential information')
    set_values_for_key(key='BaseInfo', zh='APP的基本信息', en='Application\'s essential information')

    Info(key='Info', title=get_value('BaseTitle'), level=0, info=get_value('BaseInfo'),
         result="\n".join(results)).description()


def reverse(filePath, appBinPath):
    stringDumpPath = os.path.abspath(filePath) + '/StringDump'
    strline1 = f'strings -a -T Mach-O \'{appBinPath}\' > \'{stringDumpPath}\''
    if platform.system() == 'Darwin':
        strline1 = f'strings -a \'{appBinPath}\' > \'{stringDumpPath}\''
    strline2 = f'cat \'{stringDumpPath}\' | grep \']$\' | grep \'^-\[\|^+\[\' > \'{os.path.abspath(filePath)}\'/ClassDump'
    strline3 = f'cat \'{stringDumpPath}\' | grep \'^http://\|^https://\' > \'{os.path.abspath(filePath)}\'/URLDump'
    strline4 = f'cat \'{stringDumpPath}\' | grep \'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\' > \'{os.path.abspath(filePath)}\'/IPDump'
    strline5 = f'cat \'{stringDumpPath}\' | grep @rpath | grep -v libswift > \'{os.path.abspath(filePath)}\'/RpathDump'
    cmds = [strline1, strline2, strline3, strline4, strline5]
    for strline in cmds:
        RunCMD(strline).execute()
    while len(tasks) > 0:
        for i, item in enumerate(tasks):
            item.is_running


def iOSMachO(appBinPath, filePath):
    macho = lief.MachO.parse(appBinPath, config=lief.MachO.ParserConfig.quick)
    cpuType = ''
    for i in range(0, len(macho)):
        cpuType += macho[i].header.cpu_type.name + ','
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
        'cpu_type': cpuType[:-1],
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

    with open(filePath + '/macho.json', mode='w') as f:
        json.dump(dic, f)


def iOSRpath(binPath):
    results = []
    with open(binPath, 'r') as f:
        arr = f.readlines()
    for line in arr:
        line = line.strip()
        if len(line) > 1 and line not in results:
            framework = line.split('/')[1]
            results.append(framework)
    set_values_for_key(key='THIRDLIST', zh='三方库列表', en='Thrid library list')
    set_values_for_key(key='THIRDLISTINFO', zh='查看应用使用的所有三方库', en='View all third libraries used by the application')
    Info(key='Info', title=get_value('THIRDLIST'), level=0, info=get_value('THIRDLISTINFO'),
         result="\n".join(results)).description()


def iOSAuthority(appInfoPath):
    results = []
    with open(appInfoPath, 'rb') as fp:
        pl = plistlib.load(fp)
    for key in pl.keys():
        if 'UsageDescription' in key:
            if 'UsageDescriptionDictionary' in key:
                dic = pl[key]
                for newKey in dic.keys():
                    results.append(newKey + ":" + dic[newKey])
            else:
                results.append(key + ":" + pl[key])
    set_values_for_key(key='APPPERMISSIONSLIST', zh='应用权限列表', en='App permissions list')
    set_values_for_key(key='APPPERMISSIONSLISTINFO', zh='查看应用使用的所有权限', en='View all permissions used by the app')
    Info(key='Info', title=get_value('APPPERMISSIONSLIST'), level=0, info=get_value('APPPERMISSIONSLISTINFO'),
         result="\n".join(results)).description()


def iOSCert(appInfoPath, filePath, appBinPath):
    results = []
    set_values_for_key(key='IOSCERTIFICATEINFORMATION', zh='iOS证书信息', en='iOS certificate information')
    set_values_for_key(key='IOSCERTIFICATEINFORMATIONINFO', zh='应用打包使用的证书信息',
                       en='Certificate information used for application packaging')
    if platform.system() == 'Darwin':
        result = RunCMD(f'codesign -vv -d \'{appBinPath}\'').execute()[1].decode('utf-8', 'ignore')
        Info(key='Info', title=get_value('IOSCERTIFICATEINFORMATION'), level=0,
             info=get_value('IOSCERTIFICATEINFORMATIONINFO'), result=result).description()
    else:
        results.append('Executable=' + appBinPath)
        with open(appInfoPath, 'rb') as fp:
            pl = plistlib.load(fp)
        for key in pl.keys():
            if 'CFBundleIdentifier' == key:
                results.append('Identifier=' + pl[key])
        with open(filePath + '/macho.json', 'r') as f:
            dic = json.loads(f.read())
            if ',' in dic['cpu_type']:
                results.append('Format=app bundle with Mach-O universal (' + dic['cpu_type'].replace(',', ' ') + ')')
            else:
                results.append('Format=Mach-O thin (' + dic['cpu_type'] + ')')
        teamID = ''
        result = ''
        with open(filePath + '/StringDump', 'r') as f:
            arr = f.readlines()
            for i, line in enumerate(arr):
                line = line.strip()
                if 'Apple iPhone OS Application Signing' in line and 'Apple iPhone OS Application Signing' not in result:
                    result += 'Authority=Apple iPhone OS Application Signing\n'
                    results.append('Authority=Apple iPhone OS Application Signing')
                if 'Apple iPhone Certification Authority' in line and 'Apple iPhone Certification Authority' not in result:
                    result += 'Authority=Apple iPhone Certification Authority\n'
                    results.append('Authority=Apple iPhone Certification Authority')
                if 'Apple Distribution:' in line and 'Apple Distribution:' not in result:
                    line = line.strip()
                    start = line.find('Apple Distribution:')
                    end = line.find(')', len(line) - 12)
                    result += 'Authority=' + line[start:end] + '\n'
                    results.append('Authority=' + line[start:end])
                if 'Apple Worldwide Developer Relations Certification Authority' in line and 'Apple Worldwide Developer Relations Certification Authority' not in result:
                    result += 'Authority=Apple Worldwide Developer Relations Certification Authority\n'
                    results.append('Authority=Apple Worldwide Developer Relations Certification Authority')
                if '<key>com.apple.developer.team-identifier</key>' in line:
                    teamID = arr[i + 1].replace('<string>', '').replace('</string>', '')
        results.append('Authority=Apple Root CA')
        if teamID != '':
            results.append('TeamIdentifier=' + teamID.strip())
        Info(key='Info', title=get_value('IOSCERTIFICATEINFORMATION'), level=0,
             info=get_value('IOSCERTIFICATEINFORMATIONINFO'), result="\n".join(results)).description()
