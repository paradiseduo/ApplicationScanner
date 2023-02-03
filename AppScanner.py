#!/usr/bin/python3
# -*- coding:utf-8 -*-
import getopt
import sys

from lib import translation
from lib.apk import apkScan
from lib.ipa import ipaScan
from lib.sdk import *

Version = 2.4

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
        python3 AppScanner.py -i *.apk/*.ipa/*.aab
    
        -h help
        -i <inputPath>
        -s save cache (Default clear cache)
        -l language ['zh', 'en'] (Default zh)
        -f <CheckList Path>
    ''', style='green')


translation.init()
translation.changeLanguage('zh')

def main(argv):
    inputfile = ''
    checklist = ''
    try:
        opts, args = getopt.getopt(argv, "hsi:l:f:", ["inputPath=language=checklist="])
    except getopt.GetoptError:
        printUse()
        sys.exit(2)

    save = False
    for (opt, arg) in opts:
        if opt == '-h':
            printUse()
            sys.exit()
        elif opt in ("-i", "--inputPath"):
            inputfile = arg
        elif opt in ("-l", "--language"):
            translation.changeLanguage(arg)
        elif opt in ("-f", "--checklist"):
            checklist = arg
        elif opt == '-s':
            save = True

    if len(inputfile) > 0:
        if not os.path.exists(inputfile):
            console.print('File not exist!', style='red bold')
            sys.exit(0)
        if inputfile.endswith('.apk') or inputfile.endswith('.aab'):
            apkScan(inputfile, save)
        elif inputfile.endswith('.ipa'):
            ipaScan(inputfile, save)
        elif inputfile.endswith('.framework'):
            checkFramework(inputfile, checklist)
        elif inputfile.endswith('.aar'):
            checkAar(inputfile, checklist)
        elif inputfile.endswith('.a'):
            checkA(inputfile, checklist)
        elif inputfile.endswith('.so'):
            checkSo(inputfile, checklist)
        elif inputfile.endswith('.jar'):
            checkJar(inputfile, checklist)
        else:
            console.print('Application must be *.apk or *.ipa', style='red bold')
            sys.exit(2)
    else:
        printUse()
        sys.exit(2)


if __name__ == '__main__':
    main(sys.argv[1:])
