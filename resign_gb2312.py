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
    # ��׿apk
    if isapk(PACK_ORIGIN):
        for root, dirs, files in os.walk(UNPACK_DIR):
            for dirname in dirs:
                if dirname=='META-INF':
                    fulldir = os.path.join(root, dirname)
                    print_green(fulldir)
                    removeDir(fulldir)
                    print_green('ǩ��ɾ���ɹ���')
                    return
        print_red('ǩ��ɾ��ʧ�ܣ�')
    
    # iOS ipa
    elif isipa(PACK_ORIGIN):
        for root, dirs, files in os.walk(UNPACK_DIR):
            for dirname in dirs:
                if dirname == '_CodeSignature':
                    fulldir = os.path.join(root, dirname)
                    print_green(fulldir)
                    removeDir(fulldir)
                    print_green('ǩ��ɾ���ɹ���')

            for filename in files:
                if filename == 'embedded.mobileprovision':
                    filename = os.path.join(root, filename)
                    os.system("cp " + IPA_PROV + " " + filename)
                    print_green('�滻PROV�ɹ���')

    else:
        print_red('�˽ű����ܴ���ipa��apk��')
        sys.exit(0)

# ǩ��apk
def signapk(packname):
    execstr = "jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore " + APK_KEY + " -storepass " + APK_PASS + " " + PACK_NEW + " " + APK_ALIAS
    status = os.system(execstr)
    if status == 0:
        print_green('ǩ���ɹ���')
        print_green(packname)
    else:
        print_red('ǩ��ʧ�ܣ�')

# ǩ��ipa
def signipa(packname):
    execstr = "/usr/bin/codesign -f -s \"" + IPA_CER + "\" --entitlements " + IPA_ENT + " " + IPA_APP
    os.system(execstr)
    print_green('ǩ����ɣ�')
    execstr = "/usr/bin/codesign --verify " + IPA_APP
    print_green('��֤ǩ����ɣ�')

# ���ǩ���ļ��Ƿ����
def checksigner():
    if isapk(PACK_ORIGIN):
        if not os.path.exists(APK_KEY):
            print_red('ǩ���ļ�����ʧ��:')
            print_red(APK_KEY)
            sys.exit(0)
        else:
            print_green('�ҵ�ǩ���ļ���')
            print_green(APK_KEY)

    elif isipa(PACK_ORIGIN):
        # ipaǩ��ֻ����mac��ִ��
        if isWindows():
            print_red('ipa����ǩ��ֻ����mac�Ͻ���')
            sys.exit(0)

        if not os.path.exists(IPA_PROV):
            print_red('ǩ���ļ�����ʧ��:')
            print_red(IPA_PROV)
            sys.exit(0)
        else:
            print_green('�ҵ�ǩ���ļ���')
            print_green(IPA_PROV)

        if not os.path.exists(IPA_ENT):
            print_red('ǩ���ļ�����ʧ��:')
            print_red(IPA_ENT)
            sys.exit(0)
        else:
            print_green('�ҵ�ǩ���ļ���')
            print_green(IPA_ENT)

        global IPA_APP
        for root, dirs, files in os.walk(UNPACK_DIR):
            for dirname in dirs:
                if IPA_APP == dirname:
                    print_green('�ҵ�APP�ļ�:')
                    IPA_APP = os.path.join(root, dirname)
                    print_green(IPA_APP)
        if not os.path.exists(IPA_APP):
            print_red('����APP�ļ�ʧ�ܣ�')
            print_red(IPA_APP)
            sys.exit(0)



####################
# main
####################

if len(sys.argv) <> 3:
    print_red('��������')
    print_green('eg. python resign.py 2333 d:/redbird.apk')
    sys.exit(1)

# apkǩ��
APK_KEY = os.path.join(os.getcwd(), 'customer-hn787878-20160315.keystore')
APK_ALIAS = 'customer'
APK_PASS = 'hn787878'

# ipaǩ��
IPA_PROV = os.path.join(os.getcwd(), 'embedded.mobileprovision')
IPA_CER = 'iPhone Distribution: Beijing TianRuiDiAn Network Technology Co,Ltd.'
IPA_ENT = os.path.join(os.getcwd(), 'Entitlements.plist')
IPA_APP = 'MixProject-mobile.app'

# ĸ��
PACK_ORIGIN = sys.argv[2]
if not os.path.exists(PACK_ORIGIN):
    print_red(PACK_ORIGIN + 'ĸ���ļ�����ʧ�ܣ�')
    sys.exit(1)

# ������id
AGENT_ID = sys.argv[1]

# ǩ����
PACK_NEW = newname(AGENT_ID, PACK_ORIGIN)

# ��ѹĿ¼
UNPACK_DIR = PACK_NEW[:PACK_NEW.rindex('.')]
print_green('�����...')
print_green(PACK_ORIGIN)
unzip(PACK_ORIGIN, UNPACK_DIR)
print_green('�ɹ���ѹ��: ')
print_green(UNPACK_DIR)

# ���ǩ��
print_green('���ǩ��...')
checksigner()

# ���������ļ�
print_green('��λconfig.json�ļ�...')
CONFIG_FILE = findconfig(UNPACK_DIR)
print_green('�ҵ������ļ�: ')
print_green(CONFIG_FILE)

# д��������ֶ�
print_green('д��������ֶ�...')
writeJson(CONFIG_FILE, 'agent', AGENT_ID)

# ɾ����ǩ��
print_green('ɾ��ǩ��...')
removeSign()

####################
# ��׿��ǩ��
if isapk(PACK_ORIGIN):
    # ѹ��
    print_green('���´����...')
    zip_dir(UNPACK_DIR, PACK_NEW)
    print_green(PACK_NEW)
    # ǩ��
    print_green('����ǩ����...')
    signapk(PACK_NEW)

####################
# iOS��ǩ��
elif isipa(PACK_ORIGIN):
    # ǩ��
    print_green('����ǩ����...')
    signipa(PACK_NEW)
    # ѹ��
    print_green('���´����...')
    zip_dir(UNPACK_DIR, PACK_NEW)
    print_green(PACK_NEW)

# ���������ֳ�
restoreENV()

