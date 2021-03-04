#!/usr/bin/python3
# -*- coding:utf-8 -*-
import termcolor

LEVEL = {
    0: '信息',
    1: '低危',
    2: '中危',
    3: '高危',
    4: '紧急'
}


class Info:
    def __init__(self, key='Info', title='', level=0, info='', result=''):
        self.title = title
        self.level = level
        self.info = info
        self.result = result
        self.key = key
    
    def description(self):
        if len(self.result) > 0:
            levelColor = 'white'
            if self.level == 1:
                levelColor = 'cyan'
            elif self.level == 2:
                levelColor = 'magenta'
            elif self.level == 3 or self.level == 4:
                levelColor = 'red'
            termcolor.cprint('\n检测项目: ' + self.title, 'green')
            termcolor.cprint('项目描述: ' + self.info, 'yellow')
            termcolor.cprint('危险等级: ' + LEVEL[self.level], levelColor)
            termcolor.cprint('扫描结果: \n' + self.result, 'white')