#coding=utf-8 

import json
import sys

#修改默认编码处理中文异常问题
reload(sys)
sys.setdefaultencoding('utf-8')

# 读文件
filename = "test.json"
fp = open(filename, 'r')
filestr = fp.read()
fp.close()
print filestr
print '--------'

#增加代理商字段
dictstr=json.loads(filestr)
dictstr['agent']='abc'
filestr =json.dumps(dictstr, ensure_ascii=False)
print filestr
print '--------'

#写文件
fp = open('test2.json', 'w')
fp.write(filestr)
fp.close()

print '--------'
print sys.argv[0]
print sys.argv[1]
print sys.argv
print len(sys.argv)
print '--------'
