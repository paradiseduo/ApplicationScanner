#!/usr/bin/python3
# -*- coding:utf-8 -*-
import random
import os
import string
import subprocess
import re
import json
import lief

# 文件白名单，如果不需要可以清空，也可以自行添加
whiteList = ['facebook', 'tencent', 'huawei', 'aliyun', 'android/support', 'xiaomi', 'vivo', 'oppo', 'airbnb', 'amap',
             'alipay', 'google', 'okhttp3', 'retrofit2', 'mozilla', 'freemarker', 'alibaba', 'qihoo', 'gson', 'jpush',
             'bugtags', 'trello', 'bumptech', 'jiguang', 'github', 'umeng', 'greenrobot', 'eclipse', 'bugly', 'sina',
             'weibo', 'j256', 'taobao/weex', 'iflytek', 'androidx/', 'meizu', 'io/agora', 'ijkplayer', 'sqlcipher',
             'cmic/sso', 'shanyan_sdk', 'svgaplayer', 'io/flutter', 'bytedance', 'kotlin', 'org/apache', 'org/aspectj',
             'baidu', 'youzan', 'jdpaysdk', 'qq', 'kotlinx', '/android/']

tasks = []


class RunCMD:
    def __init__(self):
        self.p = None
        self.cmd = None

    def run_cmd(self):
        self.p = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        tasks.append(self)
        return self.p.communicate()

    @property
    def is_running(self):
        if self.p.poll() is None:
            return True
        else:
            tasks.remove(self)
            return False

    def stop(self):
        self.p.kill()
        tasks.remove(self)

    def log(self):
        return ''.join([str(item, encoding='utf-8') for item in self.p.communicate()])


def cmdString(strline):
    return strline + ' | ' + grepThirdFile()


def randomStr(num):
    return '_' + ''.join(random.sample(string.ascii_letters + string.digits, num))


def getAPKFiles(dir):
    filesArray = []
    dirlist = os.walk(dir)
    jsFiles = []
    for root, dirs, files in dirlist:
        for file in files:
            path = os.path.join(root, file)
            if file.endswith('.smali') or file.endswith('.so') or file.endswith('.xml') or file.endswith(
                    '.yml') or file.endswith('.html'):
                if '/original/' not in path:
                    filesArray.append(path)
            if file.endswith('.js'):
                jsFiles.append(path)
            if file.endswith('.jsbundle') or file.endswith('.rnbundle'):
                path = changeJSBundleFile(path)
                jsFiles.append(path)
    newPaths = jsBeautify(jsFiles)
    filesArray = filesArray + newPaths
    return filesArray


def getFileName(path):
    if len(path) > 0:
        items = str(path).split('/')
        dir = ''
        start = -1
        for i in range(len(items)):
            if 'smali' in items[i] and '.smali' not in items[i]:
                start = i
            if start != -1 and start != i:
                dir += items[i] + '.'
        return dir[:-1]
    else:
        return ''


def jsBeautify(jsFiles):
    newFiles = []
    for file in jsFiles:
        beautifyFile = file[:-3] + '1.js'
        newFiles.append(beautifyFile)
        strline = 'js-beautify ' + file + ' > ' + beautifyFile
        runner = RunCMD()
        runner.cmd = strline
        runner.run_cmd()
    while len(tasks) > 0:
        for item in tasks:
            item.is_running
    return newFiles


def changeJSBundleFile(filename):
    portion = os.path.splitext(filename)
    newName = filename
    if portion[1] == '.jsbundle' or portion[1] == '.rnbundle':
        newName = str(portion[0]) + '.js'
        os.rename(filename, newName)
    return newName


def getURL(line):
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    urls = re.findall(pattern, line[:-1])
    return urls


def grepThirdFile():
    return "grep -v '" + '\|'.join(whiteList) + "'"


def getSmalis(arrs):
    paths = []
    for item in arrs:
        if '.smali:' in item:
            path = item.split(':')[0]
            if path not in paths:
                paths.append(path)
    return paths


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


def iOSAuthority(filePath):
    strline = "/usr/libexec/PlistBuddy -c 'Print' " + filePath
    p = subprocess.Popen(strline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()[0].decode('utf-8', 'ignore')
    arr = out.split('\n')
    result = ''
    for item in arr:
        if 'Description' in item:
            ar = item.split('=')
            result += ar[0].strip() + ':' + ar[1].strip() + '|'
    return result


def iOSRpath(filePath, binPath):
    result = ''
    out = os.popen('cd '+filePath +" && ls | grep '.bundle'").readlines()
    for line in out:
        result += line + '|'
    p = subprocess.Popen('otool -L ' + binPath + '| grep @rpath | grep -v libswift', shell=True, stdout=subprocess.PIPE)
    aa = p.communicate()[0].decode('utf-8', 'ignore')
    arr = aa.split('\n')
    for line in arr:
        if len(line) > 1:
            framework = line.split('/')[1]
            result += framework + '|'
    return result[:-1]