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
    print 'error: ', '\033[0;31m', msg, '\033[0m'
    return

def print_green(msg):
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
    return 0

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
    for root, dirs, files in os.walk(UNPACK_DIR):
        for dir in dirs:
            if dir=='META-INF':
                fulldir = os.path.join(root, dir)
                print_green('删除签名...')
                print_green(fulldir)
                removeDir(fulldir)
                print_green('签名删除成功！')
                return
    print_red('签名删除失败！')

# 签名
def signpack(packname):
    execstr = "jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore " + KEYSTORE + " -storepass " + PASSWORD + " " + NEW_PACK + " " + ALIAS
    status = os.system(execstr)

# main
if len(sys.argv) <> 3:
    print_red('参数错误')
    print_green('eg. python resign.py 2333 d:/redbird.apk')
    sys.exit(1)

# 签名账号
KEYSTORE = 'customer-hn787878-20160315.keystore'
ALIAS = 'customer'
PASSWORD = 'hn787878'

# 母包
ORIGIN_PACK = sys.argv[2]

# 代理商id
SIGN_CODE = sys.argv[1]

# 签名包
NEW_PACK = newname(SIGN_CODE, ORIGIN_PACK)

# 解压目录
UNPACK_DIR = NEW_PACK[:NEW_PACK.rindex('.')]
print_green('解包中...')
print_green(ORIGIN_PACK)
unzip(ORIGIN_PACK, UNPACK_DIR)
print_green('成功解压到: ')
print_green(UNPACK_DIR)

# 查找配置文件
print_green('定位config.json文件...')
CONFIG_FILE = findconfig(UNPACK_DIR)
print_green('找到配置文件: ')
print_green(CONFIG_FILE)

# 写入代理商字段
print_green('写入代理商字段...')
writeJson(CONFIG_FILE, 'agent', SIGN_CODE)

# 删除旧签名
removeSign()

# 压缩
print_green('重新打包中...')
zip_dir(UNPACK_DIR, NEW_PACK)
print_green(NEW_PACK)

# 签名
print_green('重新签名中...')

# 清理作案现场
restoreENV()

