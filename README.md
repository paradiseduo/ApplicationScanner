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

                             By ParadiseDuo  [Version: 1.0]

Usage:
    python3 AppScanner.py -i *.apk/*.ipa

    -h help
    -i <inputPath>
    -s save cache (Default clear cache)
```
## Requirement
* Only support Mac/Linux, no Windows version.
* Make sure have python3.x and Java 11 installed in your computer.
* Install libplist (Only Linux Require)
	```bash
	yum install libplist-devel libplist
	or
	apt install libplist-utils
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
> python3 AppScanner.py
Usage:
    python3 AppScanner.py -i *.apk/*.ipa

    -h help
    -i <inputPath>
    -s save cache (Default clear cache) 
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

                             By ParadiseDuo  [Version: 1.0]
I: Using Apktool 2.5.0 on test.apk
I: Loading resource table...
I: Decoding AndroidManifest.xml with resources...
I: Loading resource table from file: /Users/xmly/Library/apktool/framework/1.apk
I: Regular manifest package...
I: Decoding file-resources...
I: Decoding values */* XMLs...
I: Baksmaling classes.dex...
I: Copying assets and libs...
I: Copying unknown files...
I: Copying original files...

检测项目: 签名信息
项目描述: 签名验证详细信息
危险等级: 信息
扫描结果:
Verifies
Verified using v1 scheme (JAR signing): true
Verified using v2 scheme (APK Signature Scheme v2): true
Verified using v3 scheme (APK Signature Scheme v3): false
Verified using v4 scheme (APK Signature Scheme v4): false
Verified for SourceStamp: false
Number of signers: 1
Signer #1 certificate DN: C=US, O=Android, CN=Android Debug
Signer #1 certificate SHA-256 digest: 11fd518047589c9bfcbbbb45711917d77ee92f214cae3139a746d1049f635190
Signer #1 certificate SHA-1 digest: a579de8a6dbd5edb575823c5b86ace003df6dc40
Signer #1 certificate MD5 digest: 93a85244b2463b52f682de6972fc331b
Signer #1 key algorithm: RSA
Signer #1 key size (bits): 2048
Signer #1 public key SHA-256 digest: 9b1f3a1ac030576fb25b45d3f4a55025044c7de6bd2b1ebaa3ac89968ab06d2d
Signer #1 public key SHA-1 digest: aa41abb46b7a14d386a13953c8a587e538f97096
Signer #1 public key MD5 digest: b2cdc1649e14715779251f33030887cb


检测项目: 证书指纹
项目描述: 证书指纹信息
危险等级: 信息
扫描结果:
所有者: C=US, O=Android, CN=Android Debug
发布者: C=US, O=Android, CN=Android Debug
序列号: 1
生效时间: Wed Jul 01 18:00:50 CST 2020, 失效时间: Fri Jun 24 18:00:50 CST 2050
证书指纹:
	 SHA1: A5:79:DE:8A:6D:BD:5E:DB:57:58:23:C5:B8:6A:CE:00:3D:F6:DC:40
	 SHA256: 11:FD:51:80:47:58:9C:9B:FC:BB:BB:45:71:19:17:D7:7E:E9:2F:21:4C:AE:31:39:A7:46:D1:04:9F:63:51:90
签名算法名称: SHA1withRSA
主体公共密钥算法: 2048 位 RSA 密钥
版本: 1


检测项目: 权限信息
项目描述: 应用使用权限信息
危险等级: 信息
扫描结果:
  包名: com.hijack.demo.hijack
  使用权限列表
      android.permission.ACCESS_COARSE_LOCATION
      ...
      com.heytap.mcs.permission.RECIEVE_MCS_MESSAGE
      
检测项目: Zip文件解压目录遍历检测
项目描述: 检测Apk中是否存在Zip文件解压目录遍历漏洞
危险等级: 高危
扫描结果:
com.hijack.demo.hijack.TestZip.smali : 74

检测项目: 截屏攻击风险检测
项目描述: 检测App是否存在截屏攻击风险检测
危险等级: 低危
扫描结果:
com.hijack.demo.hijack.QQActivity.smali

检测项目: 网络端口开放威胁检测
项目描述: 检测App中是否存在网络端口开放风险
危险等级: 低危
扫描结果:
com.hijack.demo.hijack.UdpClient$1.smali UDP : 76
com.hijack.demo.hijack.SocketServer.smali TCP : 31

检测项目: WebView远程代码执行检测
项目描述: 检测App应用的Webview组件中是否存在远程代码执行漏洞
危险等级: 高危
扫描结果:
com.hijack.demo.hijack.MyWebView.smali : 129
```

## Next Step
iOS scan coming soon...
