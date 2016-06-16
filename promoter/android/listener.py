#encoding:utf-8    
from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler 
import io,shutil,urllib     
import sys,os,time
import commands
class MyHttpHandler(BaseHTTPRequestHandler):     
    def do_GET(self):
        #不使用GET方式
        '''
        if '?' in self.path:#如果带有参数  
            query = urllib.splitquery(self.path)
            action = query[0]
            if query[1] :#接收get参数
                queryParams = {}
                for qp in query[1].split('&'):
                    kv = qp.split('=')
                    queryParams[kv[0]] = urllib.unquote(kv[1]).decode("utf-8",'ignore')

            content = str(queryParams)
            #指定返回编码
            enc = "UTF-8"
            content = content.encode(enc)
            f = io.BytesIO()
            f.write(content)
            f.seek(0)
            self.send_response(200)
            self.send_header("Content-type","text/html; charset=%s" % enc)
            self.send_header("Content-Length",str(len(content)))
            self.end_headers()
            shutil.copyfileobj(f,self.wfile)
        '''

    def do_POST(self):     
        datas = self.rfile.read(int(self.headers['content-length']))
        #指定编码方式
        datas = urllib.unquote(datas).decode("utf-8",'ignore')
        #将参数转换为字典
        datas = transDicts(datas)
        if datas.has_key('code'):
            code = str(datas['code']);
            NOW = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
            writeTolog(NOW)
            writeTolog("start to build dakulong_" + code + ".apk")
            cmd = "python " + os.path.join(ROOTPATH,"apk-resign.py") + " " + code
            status = os.system(cmd)
            #status, output = commands.getstatusoutput(cmd)
            if status == 0 :
                message = "dakulong_" + code + ".apk build success"
            elif status == 1 :
                message = "pop number must be a number"
            elif status == 2 :
                message = "dakulong.apk missing"
            elif status == 3 :
                message = "dkl.keystore missing"
            elif status == 4 :
                message = "apk sign fail"
                
            content = "{\"status\":" + str(status) + ",\"message\": " + message +"}"
            #指定返回编码
            enc = "UTF-8"
            #reload(sys)
            #sys.setdefaultencoding('gb18030')
            content = content.encode(enc)
            f = io.BytesIO()
            f.write(content)
            f.seek(0)
            self.send_response(200)
            self.send_header("Content-type","text/html; charset=%s" % enc)
            self.send_header("Content-Length",str(len(content)))
            self.end_headers()
            shutil.copyfileobj(f,self.wfile)
            writeTolog(message)
            writeTolog("-------------------------------------------------")
            
def writeTolog(log):
    f = open(os.path.join(ROOTPATH,"log.txt"),"a+");
    f.write(log + "\n");
    f.close()
    print log

def transDicts(params):
    dicts={}
    if len(params)==0:
        return
    params = params.split('&')
    for param in params:
        dicts[param.split('=')[0]]=param.split('=')[1]
    return dicts

ROOTPATH = os.path.dirname(sys.argv[0])
httpd = HTTPServer(('',8080),MyHttpHandler)     
print("Server started on 127.0.0.1,port 8080.....") 
print "-------------------------------------------------"    
httpd.serve_forever() 