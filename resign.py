# coding=utf-8 

import zipfile
import sys, os
import platform

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
    print '\033[0;31m', msg, '\033[0m'
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


# main
if len(sys.argv) <> 3:
    print_red('参数错误')
    print_green('eg. python resign.py 2333 d:/redbird.apk')
    sys.exit(1)

TARGET_NAME = sys.argv[2]
print_red(isipa(TARGET_NAME))
print_red(isapk(TARGET_NAME))

