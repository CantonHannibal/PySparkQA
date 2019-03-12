# 客户端一
import socket

obj = socket.socket()
obj.connect(('127.0.0.1', 8002))
print('1')
obj.send(str('fuck you1').encode())
content = str(obj.recv(1024), encoding='utf-8')
print(content,'1')

obj.close()

# obj2 = socket.socket()
# obj2.connect(('127.0.0.1', 8003))
# content = str(obj2.recv(1024), encoding='utf-8')
# print(content,'2')
#
# obj2.close()
#
#
#
# obj3 = socket.socket()
# obj3.connect(('127.0.0.1', 8004))
# content = str(obj3.recv(1024), encoding='utf-8')
# print(content,'3')
#
# obj3.close()


