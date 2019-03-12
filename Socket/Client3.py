# 客户端三
import socket

obj3 = socket.socket()
obj3.connect(('127.0.0.1', 8004))
content = str(obj3.recv(1024), encoding='utf-8')
print(content)

obj3.close()