#!/usr/bin/python3
# -*- coding:utf-8 -*-
import shutil
import termcolor
from lib.tools import *

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
        termcolor.cprint('Authority ' + appInfoPath, 'white')
        iOSAuthority(appInfoPath)
        termcolor.cprint('Finish', 'green')
        termcolor.cprint('Rpath ' + appBinPath, 'white')
        iOSRpath(filePath, appBinPath)
        termcolor.cprint('Finish', 'green')
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
