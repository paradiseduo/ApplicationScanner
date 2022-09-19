import shutil

from lib.info import Info
from lib.tools import *
from lib.translation import *
from pathlib import Path

dx = str(Path(__file__).parents[1] / 'ThirdTools/dx.jar')
baksmali = str(Path(__file__).parents[1] / 'ThirdTools/baksmali-2.5.2.jar')


def checkJar(inputfile, checklist):
    console.print('\n[bold magenta]Checking ' + inputfile + '[/bold magenta]')
    name = inputfile.split('/')[-1].replace('.jar', '')
    dexPath = f'{name}.dex'
    RunCMD(f'java -jar {dx} --min-sdk-version=26 --dex --output={dexPath} \'{inputfile}\'').execute()
    RunCMD(f'java -jar {baksmali} disassemble {dexPath} -o cachePath').execute()
    RunCMD(f'rm -rf {dexPath}').execute()
    scan('./cachePath', checklist, [])
    console.print('\n[bold magenta]Clean cache...[/bold magenta]')
    shutil.rmtree('./cachePath')
    console.print('[bold green]Finish[/bold green]')


def checkSo(inputfile, checklist):
    console.print('\n[bold magenta]Checking ' + inputfile + '[/bold magenta]')
    scan(inputfile, checklist, [inputfile])


def checkA(inputfile, checklist):
    console.print('\n[bold magenta]Checking ' + inputfile + '[/bold magenta]')
    scan(inputfile, checklist, [inputfile])


def checkAar(inputfile, checklist):
    console.print('\n[bold magenta]Checking ' + inputfile + '[/bold magenta]')
    RunCMD(f'unzip -o \'{inputfile}\' -d ./cachePath').execute()
    jarArray = []
    soArray = []
    for (dir_path, dir_names, file_names) in os.walk('./cachePath'):
        for file_name in file_names:
            ppp = str(os.path.join(dir_path, file_name))
            if ppp.endswith('.jar'):
                jarArray.append(ppp)
            if ppp.endswith('so'):
                soArray.append(ppp)
    for p in jarArray:
        name = p.split('/')[-1].replace('.jar', '')
        dexPath = f'cachePath/{name}.dex'
        RunCMD(f'java -jar {dx} --min-sdk-version=26 --dex --output={dexPath} \'{p}\'').execute()
        RunCMD(f'java -jar {baksmali} disassemble {dexPath} -o cachePath').execute()
        RunCMD(f'rm -rf {dexPath} {p}').execute()
    scan('./cachePath', checklist, soArray)
    console.print('\n[bold magenta]Clean cache...[/bold magenta]')
    shutil.rmtree('./cachePath')
    console.print('[bold green]Finish[/bold green]')


def checkFramework(inputfile, checklist):
    console.print('\n[bold magenta]Checking ' + inputfile + '[/bold magenta]')
    machOArr = []
    for (dir_path, dir_names, file_names) in os.walk(inputfile):
        for file_name in file_names:
            ppp = str(os.path.join(dir_path, file_name))
            if len(os.path.splitext(file_name)[1]) == 0:
                machOArr.append(ppp)
    scan(inputfile, checklist, machOArr)


def scan(inputfile, checklist, machOArr):
    set_values_for_key(key='TFFC', zh='以下文件包含', en='The following files contain')
    with open(checklist, 'r') as f:
        for line in f:
            result = []
            line = line.strip()
            if re.compile(u'[\u4e00-\u9fa5]').search(line):
                # 转小端
                s = str(line.encode('unicode_escape').decode('utf-8')).replace('\\u', '')
                bitArr = re.findall(r'.{2}', s)
                jiArr = []
                ouArr = []
                for i in range(len(bitArr)):
                    if i % 2 == 1:
                        jiArr.append(bitArr[i])
                    if i % 2 == 0:
                        ouArr.append(bitArr[i])
                strrr = ''
                for i in range(len(jiArr)):
                    strrr += jiArr[i] + ouArr[i]
                for p in machOArr:
                    with open(p, 'rb') as f2:
                        sf = f2.read()
                        if sf.find(bytes().fromhex(strrr)) != -1:
                            result.append(p)
            if len(result) > 0:
                Info(key='Info', title=line, level=0, info=get_value('TFFC')+line,
                     result="\n".join(result)).description()
    with open(checklist, 'r') as f:
        for line in f:
            resultArr = []
            chinaArr = []
            source = line.strip()
            line = add_escape(source)
            chinaArr.append("grep -i -r '" + line + "' " + inputfile)
            if re.compile(u'[\u4e00-\u9fa5]').search(line):
                chinaArr.append("grep -i -r '" + add_escape(
                    str(line.encode('unicode_escape').decode('utf-8'))) + "' " + inputfile)
            for c in chinaArr:
                result = RunCMD(c).execute()[0].decode('utf-8')
                if len(result) > 0:
                    arrs = result.split('\n')
                    for item in arrs:
                        if ' matches' in item and 'Binary file ' in item:
                            if item not in resultArr:
                                resultArr.append(item)
                            continue
                        if inputfile in item:
                            file = item.split(':')[0]
                            if file not in resultArr:
                                resultArr.append(file)
                            continue
            if len(resultArr) > 0:
                Info(key='Info', title=line, level=0, info=get_value('TFFC') + line,
                     result="\n".join(resultArr)).description()