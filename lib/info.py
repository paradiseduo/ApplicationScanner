#!/usr/bin/python3
# -*- coding:utf-8 -*-
from lib.tools import *
from rich.table import Table

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
            table = Table(show_header=False, show_lines=True)
            table.add_column("Title", justify="left")
            table.add_column("Result", justify="left")
            table.add_row("检测项目", '[bold green]' + self.title + '[/bold green]')
            table.add_row("项目描述", '[bold yellow]' + self.info + '[/bold yellow]')
            table.add_row("危险等级", '[bold ' + levelColor + ']' + LEVEL[self.level] + '[/bold ' + levelColor + ']')
            table.add_row("项目描述", '[bold]' + self.result + '[/bold]')
            console.print(table)
