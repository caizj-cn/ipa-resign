# coding=utf-8 

import zipfile
import sys, os
import platform
import json

# 是否windows
def isWindows():
    return 'Windows' in platform.system()

# zip压缩
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

# zip解压
def unzip(src,des): 
    zfile = zipfile.ZipFile(src,'r')
    for filename in zfile.namelist() :
        zfile.extract(filename,des)
    return


# 高亮输出
def print_red(msg):
    if isWindows():
        print 'error: ', msg
    else:
        print 'error: ', '\033[0;31m', msg, '\033[0m'
    return

def print_green(msg):
    if isWindows():
        print msg
    else:
        print '\033[0;32m', msg, '\033[0m'
    return

# 是否apk
def isapk(filename):
    return 'apk' in filename.split('.')[-1]

# 是否ipa
def isipa(filename):
    return 'ipa' in filename.split('.')[-1]

# 重命名
def newname(prefex, oldname):
    index=oldname.rindex('.')
    return oldname[:index] + '_' + prefex + oldname[index:]

# 查找config文件
def findconfig(dirname):
    for root, dirs, files in os.walk(dirname):
        for name in files:
            if 'config.json' == name:
                return os.path.join(root, name)
    
    print_red('安装包'+ dirname + '中' +'检索config.json文件失败')
    sys.exit(0)

# 删除文件夹
def removeDir(dirname):
    if isWindows():
        os.system("rd /s /q " + dirname)
    else:
        os.system("rm -rf " + dirname)


# 清理作案现场
def restoreENV():
    print_green('清理作案现场...')
    removeDir(UNPACK_DIR)

# 向json文件中写入指定字段
def writeJson(filename, parname, value):
    if os.path.isfile(filename):
        fp = open(filename, 'r')
        filestr = fp.read()
        fp.close

        dictstr = json.loads(filestr)
        dictstr[parname] = value
        filestr = json.dumps(dictstr, ensure_ascii=False)

        fp = open(filename, 'w')
        fp.write(filestr)
        fp.close()
        return 
    else:
        print_red('文件' + filename + '不存在!')

# 删除签名
def removeSign():
    # 安卓apk
    if isapk(PACK_ORIGIN):
        for root, dirs, files in os.walk(UNPACK_DIR):
            for dirname in dirs:
                if dirname=='META-INF':
                    fulldir = os.path.join(root, dirname)
                    print_green(fulldir)
                    removeDir(fulldir)
                    print_green('签名删除成功！')
                    return
        print_red('签名删除失败！')
    
    # iOS ipa
    elif isipa(PACK_ORIGIN):
        for root, dirs, files in os.walk(UNPACK_DIR):
            for dirname in dirs:
                if dirname == '_CodeSignature':
                    fulldir = os.path.join(root, dirname)
                    print_green(fulldir)
                    removeDir(fulldir)
                    print_green('签名删除成功！')

            for filename in files:
                if filename == 'embedded.mobileprovision':
                    filename = os.path.join(root, filename)
                    os.system("cp " + IPA_PROV + " " + filename)
                    print_green('替换PROV成功！')

    else:
        print_red('此脚本仅能处理ipa和apk！')
        sys.exit(0)

# 签名apk
def signapk(packname):
    execstr = "jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore " + APK_KEY + " -storepass " + APK_PASS + " " + PACK_NEW + " " + APK_ALIAS
    status = os.system(execstr)
    if status == 0:
        print_green('签名成功！')
        print_green(packname)
    else:
        print_red('签名失败！')

# 签名ipa
def signipa(packname):
    execstr = "/usr/bin/codesign -f -s \"" + IPA_CER + "\" --entitlements " + IPA_ENT + " " + IPA_APP
    os.system(execstr)
    print_green('签名完成！')
    execstr = "/usr/bin/codesign --verify " + IPA_APP
    print_green('验证签名完成！')

# 检查签名文件是否存在
def checksigner():
    if isapk(PACK_ORIGIN):
        if not os.path.exists(APK_KEY):
            print_red('签名文件检索失败:')
            print_red(APK_KEY)
            sys.exit(0)
        else:
            print_green('找到签名文件：')
            print_green(APK_KEY)

    elif isipa(PACK_ORIGIN):
        # ipa签名只能在mac上执行
        if isWindows():
            print_red('ipa包重签名只能在mac上进行')
            sys.exit(0)

        if not os.path.exists(IPA_PROV):
            print_red('签名文件检索失败:')
            print_red(IPA_PROV)
            sys.exit(0)
        else:
            print_green('找到签名文件：')
            print_green(IPA_PROV)

        if not os.path.exists(IPA_ENT):
            print_red('签名文件检索失败:')
            print_red(IPA_ENT)
            sys.exit(0)
        else:
            print_green('找到签名文件：')
            print_green(IPA_ENT)

        global IPA_APP
        for root, dirs, files in os.walk(UNPACK_DIR):
            for dirname in dirs:
                if IPA_APP == dirname:
                    print_green('找到APP文件:')
                    IPA_APP = os.path.join(root, dirname)
                    print_green(IPA_APP)
        if not os.path.exists(IPA_APP):
            print_red('检索APP文件失败！')
            print_red(IPA_APP)
            sys.exit(0)



####################
# main
####################

if len(sys.argv) <> 3:
    print_red('参数错误')
    print_green('eg. python resign.py 2333 d:/redbird.apk')
    sys.exit(1)

# apk签名
APK_KEY = os.path.join(os.getcwd(), 'customer-hn787878-20160315.keystore')
APK_ALIAS = 'customer'
APK_PASS = 'hn787878'

# ipa签名
IPA_PROV = os.path.join(os.getcwd(), 'embedded.mobileprovision')
IPA_CER = 'iPhone Distribution: Beijing TianRuiDiAn Network Technology Co,Ltd.'
IPA_ENT = os.path.join(os.getcwd(), 'Entitlements.plist')
IPA_APP = 'MixProject-mobile.app'

# 母包
PACK_ORIGIN = sys.argv[2]
if not os.path.exists(PACK_ORIGIN):
    print_red(PACK_ORIGIN + '母包文件检索失败！')
    sys.exit(1)

# 代理商id
AGENT_ID = sys.argv[1]

# 签名包
PACK_NEW = newname(AGENT_ID, PACK_ORIGIN)

# 解压目录
UNPACK_DIR = PACK_NEW[:PACK_NEW.rindex('.')]
print_green('解包中...')
print_green(PACK_ORIGIN)
unzip(PACK_ORIGIN, UNPACK_DIR)
print_green('成功解压到: ')
print_green(UNPACK_DIR)

# 检查签名
print_green('检查签名...')
checksigner()

# 查找配置文件
print_green('定位config.json文件...')
CONFIG_FILE = findconfig(UNPACK_DIR)
print_green('找到配置文件: ')
print_green(CONFIG_FILE)

# 写入代理商字段
print_green('写入代理商字段...')
writeJson(CONFIG_FILE, 'agent', AGENT_ID)

# 删除旧签名
print_green('删除签名...')
removeSign()

####################
# 安卓重签名
if isapk(PACK_ORIGIN):
    # 压缩
    print_green('重新打包中...')
    zip_dir(UNPACK_DIR, PACK_NEW)
    print_green(PACK_NEW)
    # 签名
    print_green('重新签名中...')
    signapk(PACK_NEW)

####################
# iOS重签名
elif isipa(PACK_ORIGIN):
    # 签名
    print_green('重新签名中...')
    signipa(PACK_NEW)
    # 压缩
    print_green('重新打包中...')
    zip_dir(UNPACK_DIR, PACK_NEW)
    print_green(PACK_NEW)

# 清理作案现场
restoreENV()

