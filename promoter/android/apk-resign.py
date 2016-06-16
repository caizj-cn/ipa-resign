# !usr/bin/env python
# -*- encoding:utf-8 -*-

import zipfile
import sys,os
import platform
import commands
########################
#   调用示例
#   python apk-resign.py 推广码
#########################
 #判断系统
def isWindows():
    return 'Windows' in platform.system()

#utf8转gbk
def chineseEncode(utf8str):
    if isWindows():
        unicodeData = utf8str.decode("UTF-8")
        gbkData = unicodeData.encode("GBK")
        return gbkData
    else:
        return utf8str

#压缩zip
def zip_dir(dirname,zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
         
    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        #print arcname
        zf.write(tar,arcname)
    zf.close()
    return

#解压zip
def unzip(src,des): 
	zfile = zipfile.ZipFile(src,'r')
	for filename in zfile.namelist() :
		zfile.extract(filename,des)
	return

#main
if len(sys.argv) == 2 :
    code = sys.argv[1]
else:
    code = raw_input("please enter pop code :")

for c in code :
    if c < '0' or c > '9' :
        print "Error : pop number must be a number"
        sys.exit(1)

aliaskey = chineseEncode("北京天瑞地安网络科技有限公司")

#当前路径
ROOTPATH = os.path.dirname(sys.argv[0])
#网站目录
ABSPATH = "E:\\Big1.0\\promoter"
#解压后目录路径
DIRPATH = os.path.join(ABSPATH,"dakulong_" + code)
#apk母包路径
APKPATH = os.path.join(os.path.dirname(os.path.dirname(ABSPATH)),"dakulong.apk")
#apk子包路径
APKCHILDPATH = DIRPATH + ".apk"
#keystore路径
KEYSTOREPATH = os.path.join(ROOTPATH,"dkl.keystore")

if not os.path.isfile(APKPATH) :
    print "Error : dakulong.apk missing"
    sys.exit(2)

if not os.path.isfile(KEYSTOREPATH) :
    print "Error : dkl.keystore missing"
    sys.exit(3)

print "unziping..."
unzip(APKPATH,DIRPATH)
print "unzip apk successfully"

#删除META-INF下的签名信息
if isWindows() :
    os.system("rd /s /q " + DIRPATH + "\\META-INF")
else :
    os.system("rm -rf " + DIRPATH + "/META-INF")

print "delete previous signfile successfully"

f = file(DIRPATH + "/assets/popcode.json","w+")
f.write("{\"code\":" + code + "}")
f.close()
print "create json file successfully"

#压缩
print "ziping..."
zip_dir(DIRPATH,APKCHILDPATH)
print "zip apk successfully"

#删除目录
if isWindows() :
    os.system("rd /s /q " + DIRPATH)
else :
    os.system("rm -rf " + DIRPATH)

#签名
print "apk signing..."
EXEC = "jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore " + KEYSTOREPATH +" -storepass 000000 " + APKCHILDPATH + " " + aliaskey
status = os.system(EXEC)
#status, output = commands.getstatusoutput(EXEC)
if status == 0 :
    print "apk sign successfully"
else :
    #清理工作
    if isWindows() :
        os.system("rd /s /q " + APKCHILDPATH)
    else :
        os.system("rm -rf " + APKCHILDPATH)
    print output
    print "apk sign fail"
    sys.exit(4)


