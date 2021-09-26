#!/usr/bin/python3
# -*- coding:utf-8 -*-
import getopt
import sys
import os

from lib import translation
from lib.apk import apkScan
from lib.ipa import ipaScan
from lib.tools import console

Version = 2.2

console.print('''
                      _____                                 
    /\               / ____|                                
   /  \   _ __  _ __| (___   ___ __ _ _ __  _ __   ___ _ __ 
  / /\ \ | '_ \| '_ \\___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
 / ____ \| |_) | |_) |___) | (_| (_| | | | | | | |  __/ |   
/_/    \_\ .__/| .__/_____/ \___\__,_|_| |_|_| |_|\___|_|   
         | |   | |                                          
         |_|   |_|                                          
''', style='blink bold green')

console.print('                             [italic green]ParadiseDuo[/italic green]  [{}]'.format(Version))

def printUse():
    console.print('''
    Usage:      
        python3 AppScanner.py -i *.apk/*.ipa
    
        -h help
        -i <inputPath>
        -s save cache (Default clear cache)
        -l language ['zh', 'en'] (Default zh)
    ''', style='green')


translation.init()
translation.changeLanguage('zh')

def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hsi:l:", ["ipath=language="])
    except getopt.GetoptError:
        printUse()
        sys.exit(2)

    save = False
    for (opt, arg) in opts:
        if opt == '-h':
            printUse()
            sys.exit()
        elif opt in ("-i", "--ipath"):
            inputfile = arg
        elif opt in ("-l", "--language"):
            translation.changeLanguage(arg)
        elif opt == '-s':
            save = True

    if len(inputfile) > 0:
        if not os.path.exists(inputfile):
            console.print('File not exist!', style='red bold')
            sys.exit(0)
        if '.apk' in inputfile:
            apkScan(inputfile, save)
        elif '.ipa' in inputfile:
            ipaScan(inputfile, save)
        else:
            console.print('Application must be *.apk or *.ipa', style='red bold')
            sys.exit(2)
    else:
        printUse()
        sys.exit(2)


if __name__ == '__main__':
    main(sys.argv[1:])
