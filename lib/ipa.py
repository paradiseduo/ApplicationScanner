#!/usr/bin/python3
# -*- coding:utf-8 -*-
import plistlib
import shutil
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
    console.print('\n[magenta]Unzip ipa [/magenta][bold magenta]' + filePath + '[/bold magenta]')
    filePath, appName = ipatool(filePath)
    appBinName = appName.replace('.app', '')
    appBinPath = filePath + '/' + appName + '/' + appBinName
    appInfoPath = filePath + '/' + appName + '/' + 'Info.plist'
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


def iOSInfo(appInfoPath):
    results = []
    with open(appInfoPath, 'rb') as fp:
        pl = plistlib.load(fp)
    results.append('App名称:' + pl['CFBundleDisplayName'])
    results.append('Bundle Identifier:' + pl['CFBundleIdentifier'])
    results.append('包版本:' + pl['CFBundleShortVersionString'])
    results.append('编译版本:' + pl['CFBundleVersion'])
    results.append('SDK版本:' + pl['DTSDKName'])
    results.append('最低系统版本:' + pl['MinimumOSVersion'])
    Info(key='Info', title='APP基本信息', level=0, info='APP的基本信息', result="\n".join(results)).description()


def reverse(filePath, appBinPath):
    stringDumpPath = os.path.abspath(filePath) + '/StringDump'
    strline1 = 'strings -a -T Mach-O ' + appBinPath + " > " + stringDumpPath
    if platform.system() == 'Darwin':
        strline1 = 'strings -a ' + appBinPath + " > " + stringDumpPath
    strline2 = 'cat ' + stringDumpPath + " | grep ']$' | grep '^-\[\|^+\[' > " + os.path.abspath(
        filePath) + '/ClassDump'
    strline3 = 'cat ' + stringDumpPath + " | grep '^http://\|^https://' > " + os.path.abspath(filePath) + '/URLDump'
    strline4 = 'cat ' + stringDumpPath + " | grep '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)' > " + os.path.abspath(
        filePath) + '/IPDump'
    strline5 = 'cat ' + stringDumpPath + " | grep @rpath | grep -v libswift > " + os.path.abspath(
        filePath) + '/RpathDump'
    cmds = [strline1, strline2, strline3, strline4, strline5]
    for strline in cmds:
        runner = RunCMD()
        runner.cmd = strline
        runner.run_cmd()
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
    Info(key='Info', title='三方库列表', level=0, info='查看应用使用的所有三方库', result="\n".join(results)).description()


def iOSAuthority(appInfoPath):
    results = []
    with open(appInfoPath, 'rb') as fp:
        pl = plistlib.load(fp)
    for key in pl.keys():
        if 'UsageDescription' in key:
            results.append(key + ":" + pl[key])
    Info(key='Info', title='应用权限列表', level=0, info='查看应用使用的所有权限', result="\n".join(results)).description()


def iOSCert(appInfoPath, filePath, appBinPath):
    results = []
    if platform.system() == 'Darwin':
        strline = 'codesign -vv -d ' + appBinPath
        p = subprocess.Popen(strline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = p.communicate()[1].decode('utf-8', 'ignore')
        Info(key='Info', title='iOS证书信息', level=0, info='应用打包使用的证书信息', result=result).description()
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
        Info(key='Info', title='iOS证书信息', level=0, info='应用打包使用的证书信息', result="\n".join(results)).description()
