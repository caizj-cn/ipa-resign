#encoding:utf-8
import sys,os
import string
import commands
import zipfile
import platform
########################
#   调用示例
#   python ipa-resign.py 推广码
#########################
 #判断系统
def isWindows():
    return 'Windows' in platform.system()

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

########################################################
if isWindows() :
    print "ipa-resign can only run on os x system"
    sys.exit()

if len(sys.argv) == 2 :
    code = sys.argv[1]
else:
    code = raw_input("please enter pop code :")

for c in code :
    if c < '0' or c > '9' :
        print "Error : pop number must be a number"
        sys.exit()

SelectCer = "iPhone Distribution: Beijing TianRuiDiAn Network Technology Co,Ltd."
#当前路径
ROOTPATH = os.path.dirname(os.path.realpath(sys.argv[0]))
#ipa母包路径
IPAPATH = os.path.join(os.path.dirname(ROOTPATH),"dakulong.ipa")
#签名文件路径
MOBILEPROVISION = os.path.join(ROOTPATH,"dkl.mobileprovision")
#Entitlements文件路径
ENTITITLEMENTS = os.path.join(ROOTPATH,"Entitlements.plist")

#解压后目录路径
DIRPATH = os.path.join(ROOTPATH,"ios_dakulong_" + code)
#ipa子包路径
IPACHILDPATH = os.path.join(ROOTPATH,"dakulong_" + code + ".ipa")
#.app文件路径
APPPATH = os.path.join(DIRPATH,"Payload","HNMutlLobby\ iOS.app")
#popcode.json文件路径
POPCODE = os.path.join(DIRPATH,"Payload","HNMutlLobby iOS.app","res","popcode.json")

if not os.path.isfile(IPAPATH) :
    print "Error : dakulong.ipa missing"
    sys.exit()

if not os.path.isfile(MOBILEPROVISION) :
    print "Error : dkl.mobileprovision missing"
    sys.exit()

if not os.path.isfile(ENTITITLEMENTS) :
    print "Error : Entitlements.plist missing"
    sys.exit()

print "unziping..."
unzip(IPAPATH,DIRPATH)
print "unzip apk successfully"

os.system("rm -rf " + os.path.join(APPPATH,"_CodeSignature"))
print ">>>>>>>delete _CodeSignature"

print ">>>>>>>copy dkl.mobileprovision"
os.system("cp " + MOBILEPROVISION + " " + os.path.join(APPPATH,"embedded.mobileprovision"))

f = file(POPCODE,"w+")
f.write("{\"code\":" + code + "}")
f.close()
print "create json file successfully"

print ">>>>>>>resign"
my_commands = "/usr/bin/codesign -f -s \"" + SelectCer +"\" --entitlements " + ENTITITLEMENTS + " " + APPPATH
os.system(my_commands)
print ">>>>>>>verify begin"
os.system("/usr/bin/codesign --verify " + APPPATH)
print ">>>>>>>verify end"
#print ">>>>>>>check app info"
#os.system("codesign -vv -d " + APPPATH)

#压缩
print "ziping..."
zip_dir(DIRPATH,IPACHILDPATH)
print "zip ipa successfully"

#删除目录
os.system("rm -rf " + DIRPATH)

