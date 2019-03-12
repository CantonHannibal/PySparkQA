from main2 import *
import  socket
import time
import threading
from py2neo import Graph, Node, Relationship
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom
from QuestionRepository import *
import json
query = ModelProcess("D:/QQPCmgr/Desktop/data/data")
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
        data=json.dumps(qr.func_Router(*Args))

        sock.send(('%s \n' % data).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed.' % addr)
def start():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 9999))
    s.listen(5)
    print('Waiting for connection...')
    while True:
        sock, addr = s.accept()

        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()
if __name__=="__main__":
     start()
    # questionArr=["卧虎藏龙的分数是多少","李滨和孙红雷一起演过哪些电影","周星驰演过哪些类型的电影"]
    # qr = QuestionRepository()
    # # print(qr.func_Router(0,"卧虎藏龙"))
    # for que in questionArr:
    #     question,Args=query.analyQuery(que)
    #     print(Args)
    #     print(question,str(qr.func_Router(*Args)))


