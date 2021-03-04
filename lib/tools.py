#!/usr/bin/python3
# -*- coding:utf-8 -*-
import random
import os
import string
import subprocess
import re

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
    return strline


def randomStr(num):
    return '_' + ''.join(random.sample(string.ascii_letters + string.digits, num))


def getAPKFiles(dir):
    filesArray = []
    dirlist = os.walk(dir)
    jsFiles = []
    for root, dirs, files in dirlist:
        for file in files:
            path = os.path.join(root, file)
            if file.endswith('.smali') or file.endswith('.so') or file.endswith('.xml') or file.endswith('.yml') or file.endswith('.html'):
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
        if '$' in dir:
            return dir[:-1].split('$')[0] + '.smali'
        return dir[:-1]
    else:
        return ''


def jsBeautify(jsFiles):
    newFiles = []
    for file in jsFiles:
        beautifyFile = file[:-3]+'1.js'
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