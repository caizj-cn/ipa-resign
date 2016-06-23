# coding=utf-8 

import zipfile
import sys, os
import platform
import json

# �Ƿ�windows
def isWindows():
    return 'Windows' in platform.system()

# zipѹ��
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

# zip��ѹ
def unzip(src,des): 
    zfile = zipfile.ZipFile(src,'r')
    for filename in zfile.namelist() :
        zfile.extract(filename,des)
    return


# �������
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

# �Ƿ�apk
def isapk(filename):
    return 'apk' in filename.split('.')[-1]

# �Ƿ�ipa
def isipa(filename):
    return 'ipa' in filename.split('.')[-1]

# ������
def newname(prefex, oldname):
    index=oldname.rindex('.')
    return oldname[:index] + '_' + prefex + oldname[index:]

# ����config�ļ�
def findconfig(dirname):
    for root, dirs, files in os.walk(dirname):
        for name in files:
            if 'config.json' == name:
                return os.path.join(root, name)
    
    print_red('��װ��'+ dirname + '��' +'����config.json�ļ�ʧ��')
    sys.exit(0)

# ɾ���ļ���
def removeDir(dirname):
    if isWindows():
        os.system("rd /s /q " + dirname)
    else:
        os.system("rm -rf " + dirname)


# ���������ֳ�
def restoreENV():
    print_green('���������ֳ�...')
    removeDir(UNPACK_DIR)

# ��json�ļ���д��ָ���ֶ�
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
        print_red('�ļ�' + filename + '������!')

# ɾ��ǩ��
def removeSign():
    for root, dirs, files in os.walk(UNPACK_DIR):
        for dir in dirs:
            if dir=='META-INF':
                fulldir = os.path.join(root, dir)
                print_green('ɾ��ǩ��...')
                print_green(fulldir)
                removeDir(fulldir)
                print_green('ǩ��ɾ���ɹ���')
                return
    print_red('ǩ��ɾ��ʧ�ܣ�')

# ǩ��
def signpack(packname):
    execstr = "jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore " + KEYSTORE + " -storepass " + PASSWORD + " " + NEW_PACK + " " + ALIAS
    status = os.system(execstr)
    if status == 0:
        print_green('ǩ���ɹ���')
    else:
        print_red('ǩ��ʧ�ܣ�')
        os.remove(packname)

# main
if len(sys.argv) <> 3:
    print_red('��������')
    print_green('eg. python resign.py 2333 d:/redbird.apk')
    sys.exit(1)

# ǩ���˺�
KEYSTORE = 'customer-hn787878-20160315.keystore'
ALIAS = 'customer'
PASSWORD = 'hn787878'

# ĸ��
ORIGIN_PACK = sys.argv[2]

# ������id
SIGN_CODE = sys.argv[1]

# ǩ����
NEW_PACK = newname(SIGN_CODE, ORIGIN_PACK)

# ��ѹĿ¼
UNPACK_DIR = NEW_PACK[:NEW_PACK.rindex('.')]
print_green('�����...')
print_green(ORIGIN_PACK)
unzip(ORIGIN_PACK, UNPACK_DIR)
print_green('�ɹ���ѹ��: ')
print_green(UNPACK_DIR)

# ���������ļ�
print_green('��λconfig.json�ļ�...')
CONFIG_FILE = findconfig(UNPACK_DIR)
print_green('�ҵ������ļ�: ')
print_green(CONFIG_FILE)

# д��������ֶ�
print_green('д��������ֶ�...')
writeJson(CONFIG_FILE, 'agent', SIGN_CODE)

# ɾ����ǩ��
removeSign()

# ѹ��
print_green('���´����...')
zip_dir(UNPACK_DIR, NEW_PACK)
print_green(NEW_PACK)

# ǩ��
print_green('����ǩ����...')
signpack(NEW_PACK)

# ���������ֳ�
restoreENV()

