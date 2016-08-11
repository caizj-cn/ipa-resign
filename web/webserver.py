
from wsgiref.simple_server import make_server
from testapp import application

httpd = make_server('', 10086,  )
print 'Serving HTTP on port 10086...'

httpd.serve_forever()
