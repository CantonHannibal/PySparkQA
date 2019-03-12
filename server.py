import  socket
import time
import threading
from main2 import *
from py2neo import Graph, Node, Relationship
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
from QuestionRepository import *

query = ModelProcess("H:\hanlp(1)\hanlp\data")
qr = QuestionRepository()
def tcplink(sock, addr):

    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        question, Args = query.analyQuery(data.decode('utf-8'))
        data=str(qr.func_Router(*Args))
        sock.send(('%s' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed.' % addr)

if __name__=="__main__":
    # query = ModelProcess("H:\hanlp(1)\hanlp\data")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 9999))
    s.listen(5)
    print('Waiting for connection...')
    while True:

        sock, addr = s.accept()

        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()