# 客户端二
import socket

obj2 = socket.socket()
obj2.connect(('127.0.0.1', 8002))
print('step1')
obj2.send(str('fuck you').encode())
print('step2')
print('client has been recieved')
content = str(obj2.recv(1024), encoding='utf-8')
print('step3')
print(content,'1')

print('step4')

print('obj2 has been ')
obj2.close()