#!/usr/bin/python3
# -*- coding:utf-8 -*-
import termcolor
import getopt
import sys
import os
from lib.apk import apkScan
from lib.ipa import ipaScan

Version = 2.0

termcolor.cprint('''
                      _____                                 
    /\               / ____|                                
   /  \   _ __  _ __| (___   ___ __ _ _ __  _ __   ___ _ __ 
  / /\ \ | '_ \| '_ \\___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
 / ____ \| |_) | |_) |___) | (_| (_| | | | | | | |  __/ |   
/_/    \_\ .__/| .__/_____/ \___\__,_|_| |_|_| |_|\___|_|   
         | |   | |                                          
         |_|   |_|                                          
''', 'green')

termcolor.cprint('                             By ParadiseDuo  [Version: {}]'.format(Version), 'green')

help = '''
Usage:      
    python3 AppScanner.py -i *.apk/*.ipa

    -h help
    -i <inputPath>
    -s save cache (Default clear cache)
'''


def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hsi:", ["ipath="])
    except getopt.GetoptError:
        termcolor.cprint(help, 'green')
        sys.exit(2)

    save = False
    for (opt, arg) in opts:
        if opt == '-h':
            termcolor.cprint(help, 'green')
            sys.exit()
        elif opt in ("-i", "--ipath"):
            inputfile = arg
        elif opt == '-s':
            save = True

    if len(inputfile) > 0:
        if not os.path.exists(inputfile):
            termcolor.cprint('File not exist!', 'red')
            sys.exit(0)
        if '.apk' in inputfile:
            apkScan(inputfile, save)
        elif '.ipa' in inputfile:
            ipaScan(inputfile, save)
        else:
            termcolor.cprint('Application must be *.apk or *.ipa', 'red')
            sys.exit(2)
    else:
        termcolor.cprint(help, 'green')
        sys.exit(2)


if __name__ == '__main__':
    main(sys.argv[1:])
