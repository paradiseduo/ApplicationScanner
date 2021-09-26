# ApplicationScanner
```bash

                      _____
    /\               / ____|
   /  \   _ __  _ __| (___   ___ __ _ _ __  _ __   ___ _ __
  / /\ \ | '_ \| '_ \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
 / ____ \| |_) | |_) |___) | (_| (_| | | | | | | |  __/ |
/_/    \_\ .__/| .__/_____/ \___\__,_|_| |_|_| |_|\___|_|
         | |   | |
         |_|   |_|

                             ParadiseDuo  [2.2]

    Usage:
        python3 AppScanner.py -i *.apk/*.ipa

        -h help
        -i <inputPath>
        -s save cache (Default clear cache)
	-l language ['zh', 'en'] (Default zh)
```
## Requirement
* Only support Mac/Linux, no Windows version.
* Make sure have python3.x and Java 11 installed in your computer.
* install binutils (Only Mac Require)
   ```bash
    Mac:
    brew install binutils
   ```
* Install js-beautify

	```bash
	npm -g install js-beautify
	```

## Use
```bash
> git clone https://github.com/paradiseduo/ApplicationScanner.git
> cd ApplicationScanner
> pip install -r requirements.txt
> python3 AppScanner.py -i xxx.apk
```

## Example
You can download [test.apk](https://github.com/paradiseduo/paradiseduo/raw/master/test.apk) have a try.

**Reuslt format is filename : line number**

```bash
> python3 AppScanner.py -i test.apk

                      _____
    /\               / ____|
   /  \   _ __  _ __| (___   ___ __ _ _ __  _ __   ___ _ __
  / /\ \ | '_ \| '_ \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
 / ____ \| |_) | |_) |___) | (_| (_| | | | | | | |  __/ |
/_/    \_\ .__/| .__/_____/ \___\__,_|_| |_|_| |_|\___|_|
         | |   | |
         |_|   |_|

                             ParadiseDuo  [2.2]

Unzip apk test.apk
I: Using Apktool 2.5.0 on test.apk
I: Loading resource table...
I: Decoding AndroidManifest.xml with resources...
I: Loading resource table from file: /Users/xxx/Library/apktool/framework/1.apk
I: Regular manifest package...
I: Decoding file-resources...
I: Decoding values */* XMLs...
I: Baksmaling classes.dex...
I: Copying assets and libs...
I: Copying unknown files...
I: Copying original files...
Finish
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ 检测项目 ┃ 应用基本信息        ┃
├──────────┼─────────────────────┤
│ 项目描述 │ App的基本信息       │
├──────────┼─────────────────────┤
│ 危险等级 │ 信息                │
├──────────┼─────────────────────┤
│ 项目描述 │   minSdkVersion: 15 │
│          │   SDK版本: 26       │
│          │   版本号: 1         │
│          │   版本名: 1.0       │
└──────────┴─────────────────────┘
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 检测项目 ┃ 权限信息                                                   ┃
├──────────┼────────────────────────────────────────────────────────────┤
│ 项目描述 │ 应用使用权限信息                                           │
├──────────┼────────────────────────────────────────────────────────────┤
│ 危险等级 │ 信息                                                       │
├──────────┼────────────────────────────────────────────────────────────┤
│ 项目描述 │   包名: com.hijack.demo.hijack                             │
│          │   使用权限列表                                             │
│          │       android.permission.ACCESS_COARSE_LOCATION            │
│          │       android.permission.GET_TASKS                         │
│          │       android.permission.INTERNET                          │
│          │       android.permission.KILL_BACKGROUND_PROCESSES         │
│          │       android.permission.READ_PHONE_STATE                  │
│          │       android.permission.ACCESS_WIFI_STATE                 │
│          │       android.permission.ACCESS_NETWORK_STATE              │
│          │       android.permission.RECEIVE_BOOT_COMPLETED            │
│          │       android.permission.WRITE_EXTERNAL_STORAGE            │
│          │       android.permission.VIBRATE                           │
│          │       android.permission.WAKE_LOCK                         │
│          │       android.permission.REORDER_TASKS                     │
│          │       android.permission.READ_EXTERNAL_STORAGE             │
│          │       android.permission.WRITE_SYNC_SETTINGS               │
│          │       android.permission.READ_SYNC_SETTINGS                │
│          │       android.permission.RECORD_AUDIO                      │
│          │       android.permission.SYSTEM_ALERT_WINDOW               │
│          │       android.permission.MODIFY_AUDIO_SETTINGS             │
│          │       com.techwolf.kanzhun.app.permission.MIPUSH_RECEIVE   │
│          │       android.permission.CAMERA                            │
│          │       android.permission.READ_LOGS                         │
│          │       android.permission.ACCESS_FINE_LOCATION              │
│          │       android.permission.CHANGE_WIFI_STATE                 │
│          │       android.permission.ACCESS_LOCATION_EXTRA_COMMANDS    │
│          │       android.permission.BLUETOOTH                         │
│          │       android.permission.BLUETOOTH_ADMIN                   │
│          │       android.permission.REQUEST_INSTALL_PACKAGES          │
│          │       com.techwolf.kanzhun.app.permission.PROCESS_PUSH_MSG │
│          │       com.coloros.mcs.permission.RECIEVE_MCS_MESSAGE       │
│          │       com.heytap.mcs.permission.RECIEVE_MCS_MESSAGE        │
└──────────┴────────────────────────────────────────────────────────────┘
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 检测项目 ┃ 签名信息                                                                                               ┃
├──────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 项目描述 │ 签名验证详细信息                                                                                       │
├──────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 危险等级 │ 信息                                                                                                   │
├──────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 项目描述 │ Verifies                                                                                               │
│          │ Verified using v1 scheme (JAR signing): true                                                           │
│          │ Verified using v2 scheme (APK Signature Scheme v2): true                                               │
│          │ Verified using v3 scheme (APK Signature Scheme v3): false                                              │
│          │ Verified using v4 scheme (APK Signature Scheme v4): false                                              │
│          │ Verified for SourceStamp: false                                                                        │
│          │ Number of signers: 1                                                                                   │
│          │ Signer #1 certificate DN: C=US, O=Android, CN=Android Debug                                            │
│          │ Signer #1 certificate SHA-256 digest: 11fd518047589c9bfcbbbb45711917d77ee92f214cae3139a746d1049f635190 │
│          │ Signer #1 certificate SHA-1 digest: a579de8a6dbd5edb575823c5b86ace003df6dc40                           │
│          │ Signer #1 certificate MD5 digest: 93a85244b2463b52f682de6972fc331b                                     │
│          │ Signer #1 key algorithm: RSA                                                                           │
│          │ Signer #1 key size (bits): 2048                                                                        │
│          │ Signer #1 public key SHA-256 digest: 9b1f3a1ac030576fb25b45d3f4a55025044c7de6bd2b1ebaa3ac89968ab06d2d  │
│          │ Signer #1 public key SHA-1 digest: aa41abb46b7a14d386a13953c8a587e538f97096                            │
│          │ Signer #1 public key MD5 digest: b2cdc1649e14715779251f33030887cb                                      │
│          │                                                                                                        │
│          │                                                                                                        │
└──────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────┘
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 检测项目 ┃ 证书指纹                                                                                                 ┃
├──────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 项目描述 │ 证书指纹信息                                                                                             │
├──────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 危险等级 │ 信息                                                                                                     │
├──────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 项目描述 │ 所有者: C=US, O=Android, CN=Android Debug                                                                │
│          │ 发布者: C=US, O=Android, CN=Android Debug                                                                │
│          │ 序列号: 1                                                                                                │
│          │ 生效时间: Wed Jul 01 18:00:50 CST 2020, 失效时间: Fri Jun 24 18:00:50 CST 2050                           │
│          │ 证书指纹:                                                                                                │
│          │          SHA1: A5:79:DE:8A:6D:BD:5E:DB:57:58:23:C5:B8:6A:CE:00:3D:F6:DC:40                               │
│          │          SHA256:                                                                                         │
│          │ 11:FD:51:80:47:58:9C:9B:FC:BB:BB:45:71:19:17:D7:7E:E9:2F:21:4C:AE:31:39:A7:46:D1:04:9F:63:51:90          │
│          │ 签名算法名称: SHA1withRSA                                                                                │
│          │ 主体公共密钥算法: 2048 位 RSA 密钥                                                                       │
│          │ 版本: 1                                                                                                  │
│          │                                                                                                          │
└──────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────┘
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 检测项目 ┃ Zip文件解压目录遍历检测                   ┃
├──────────┼───────────────────────────────────────────┤
│ 项目描述 │ 检测Apk中是否存在Zip文件解压目录遍历漏洞  │
├──────────┼───────────────────────────────────────────┤
│ 危险等级 │ 高危                                      │
├──────────┼───────────────────────────────────────────┤
│ 项目描述 │ com.hijack.demo.hijack.TestZip.smali : 74 │
└──────────┴───────────────────────────────────────────┘
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 检测项目 ┃ 截屏攻击风险检测                        ┃
├──────────┼─────────────────────────────────────────┤
│ 项目描述 │ 检测App是否存在截屏攻击风险检测         │
├──────────┼─────────────────────────────────────────┤
│ 危险等级 │ 低危                                    │
├──────────┼─────────────────────────────────────────┤
│ 项目描述 │ com.hijack.demo.hijack.QQActivity.smali │
└──────────┴─────────────────────────────────────────┘
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 检测项目 ┃ 网络端口开放威胁检测                                          ┃
├──────────┼───────────────────────────────────────────────────────────────┤
│ 项目描述 │ 检测App中是否存在网络端口开放风险                             │
├──────────┼───────────────────────────────────────────────────────────────┤
│ 危险等级 │ 低危                                                          │
├──────────┼───────────────────────────────────────────────────────────────┤
│ 项目描述 │ com.hijack.demo.hijack.UdpClient$1.smali UDP : 76             │
│          │ com.hijack.demo.hijack.SocketServer.smali TCP : 31            │
│          │ com.hijack.demo.hijack.SocketServer.smali TCP : 70            │
│          │ com.hijack.demo.hijack.UdpClient$SocketThread.smali UDP : 105 │
│          │ com.hijack.demo.hijack.UdpClient$SocketThread.smali UDP : 118 │
│          │ com.hijack.demo.hijack.UdpClient$SocketThread.smali UDP : 133 │
│          │ com.hijack.demo.hijack.UdpClient$SocketThread.smali UDP : 249 │
│          │ com.hijack.demo.hijack.UdpClient$SocketThread.smali UDP : 266 │
│          │ com.hijack.demo.hijack.SocketClient.smali TCP : 31            │
│          │ com.hijack.demo.hijack.SocketClient.smali TCP : 47            │
└──────────┴───────────────────────────────────────────────────────────────┘
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 检测项目 ┃ Intent组件隐式调用风险检测                          ┃
├──────────┼─────────────────────────────────────────────────────┤
│ 项目描述 │ 检测Apk中的Intent组件是否存在隐式调用的风险         │
├──────────┼─────────────────────────────────────────────────────┤
│ 危险等级 │ 低危                                                │
├──────────┼─────────────────────────────────────────────────────┤
│ 项目描述 │ com.hijack.demo.hijack.HijackingService.smali : 185 │
│          │ com.hijack.demo.hijack.TestIntent.smali : 171       │
│          │ com.hijack.demo.hijack.TestIntent.smali : 162       │
│          │ com.hijack.demo.hijack.TestIntent.smali : 151       │
└──────────┴─────────────────────────────────────────────────────┘
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ 检测项目 ┃ IP泄露检测      ┃
├──────────┼─────────────────┤
│ 项目描述 │ 检测App泄露的IP │
├──────────┼─────────────────┤
│ 危险等级 │ 低危            │
├──────────┼─────────────────┤
│ 项目描述 │ 183.134.74.198  │
│          │ 118.25.119.177  │
│          │ 127.0.0.1       │
│          │ 127.0.0.0       │
│          │ 172.16.2.54     │
│          │ 192.168.123.32  │
└──────────┴─────────────────┘
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 检测项目 ┃ SDCARD加载dex检测                                ┃
├──────────┼──────────────────────────────────────────────────┤
│ 项目描述 │ 检测App程序中的是否存在从sdcard动态加载dex的风险 │
├──────────┼──────────────────────────────────────────────────┤
│ 危险等级 │ 低危                                             │
├──────────┼──────────────────────────────────────────────────┤
│ 项目描述 │ com.hijack.demo.hijack.DexSo.smali : 746         │
│          │ com.hijack.demo.hijack.DexSo.smali : 548         │
└──────────┴──────────────────────────────────────────────────┘
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 检测项目 ┃ Broadcast Receiver动态注册检测                ┃
├──────────┼───────────────────────────────────────────────┤
│ 项目描述 │ 检测App中是否存在动态注册Receiver风险         │
├──────────┼───────────────────────────────────────────────┤
│ 危险等级 │ 低危                                          │
├──────────┼───────────────────────────────────────────────┤
│ 项目描述 │ com.hijack.demo.hijack.QQActivity.smali : 301 │
│          │ com.hijack.demo.hijack.QQActivity.smali : 317 │
└──────────┴───────────────────────────────────────────────┘
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 检测项目 ┃ FFMPEG任意文件读取检测                                                     ┃
├──────────┼────────────────────────────────────────────────────────────────────────────┤
│ 项目描述 │ 检测App的ffmpeg so库是否存在任意文件读取漏洞                               │
├──────────┼────────────────────────────────────────────────────────────────────────────┤
│ 危险等级 │ 低危                                                                       │
├──────────┼────────────────────────────────────────────────────────────────────────────┤
│ 项目描述 │ armeabi-v7a/libijkffmpeg.so: FFmpeg version ff3.1--ijk0.6.2--20160926--001 │
│          │                                                                            │
└──────────┴────────────────────────────────────────────────────────────────────────────┘

Clean cache...
Finish
```


## Stargazers over time

[![Stargazers over time](https://starchart.cc/paradiseduo/ApplicationScanner.svg)](https://starchart.cc/paradiseduo/ApplicationScanner)

## License

This software is released under the GPL-3.0 license.
