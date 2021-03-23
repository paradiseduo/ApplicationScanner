from ..Base import Base
from ..info import Info
from ..apk import register
from ..tools import *

TITLE = '网络端口开放威胁检测'
LEVEL = 1
INFO = '检测App中是否存在网络端口开放风险'


class PortCheck(Base):
    def scan(self):
        strline = cmdString('grep -r "Ljava/net/DatagramPacket;->\|Ljava/net/DatagramSocket;->\|Ljava/net/Socket;-><init>\|Ljava/net/ServerSocket;-><init>" ' + self.appPath)
        arrs = os.popen(strline).readlines()
        results = []
        for item in arrs:
            if '.smali:' in item:
                path = item.split(':')[0]
                with open(path, 'r') as f:
                    lines = f.readlines()
                    count = len(lines)
                    name = getFileName(path)
                    for i in range(0, count):
                        line = lines[i]
                        result = ''
                        if 'Ljava/net/DatagramSocket;-><init>' in line:
                            result = name + ' UDP : ' + str(i + 1)
                        if 'Ljava/net/DatagramPacket;-><init>' in line:
                            result = name + ' UDP : ' + str(i + 1)
                        if 'Ljava/net/DatagramSocket;->receive(Ljava/net/DatagramPacket;)V' in line:
                            result = name + ' UDP : ' + str(i + 1)
                        if 'Ljava/net/DatagramSocket;->connect(Ljava/net/InetAddress;I)V' in line:
                            result = name + ' UDP : ' + str(i + 1)
                        if 'Ljava/net/ServerSocket;->accept' in line:
                            result = name + ' TCP : ' + str(i + 1)
                        if 'Ljava/net/Socket;->connect' in line:
                            result = name + ' TCP : ' + str(i + 1)
                        if 'Ljava/net/Socket;-><init>' in line:
                            result = name + ' TCP : ' + str(i + 1)
                        if 'Ljava/net/ServerSocket;-><init>' in line:
                            result = name + ' TCP : ' + str(i + 1)
                        if result not in results and result != '':
                            results.append(result)
        Info(key=self.__class__, title=TITLE, level=LEVEL, info=INFO, result='\n'.join(results)).description()


register(PortCheck)