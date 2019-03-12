
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('127.0.0.1', 9999))

print(client.recv(1024).decode('utf-8'))

while True:

    sendmsg = input("input:")

    if sendmsg=='q':
        break

    sendmsg = sendmsg

    client.sendall(sendmsg.encode("utf-8"))
    msg = client.recv(1024)

    print(msg.decode("utf-8"))
# for data in [b'Michael', b'Tracy', b'Sarah']:
#     # 发送数据:
#     s.send(data)
#     print(s.recv(1024).decode('utf-8'))
# s.send(b'exit')
# s.close()


