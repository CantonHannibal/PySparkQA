import socket

socketserver = socket.socket()
host = '0.0.0.0'
port = 9092

socketserver.bind((host, port))

socketserver.listen(5)


clientsocket,addr = socketserver.accept()


while True:


    recvmsg = clientsocket.recv(1024)

    strData = recvmsg.decode("utf-8")

    if strData=='q':
        break
    print("Roger:"+strData)
    msg = input("reply:")

    clientsocket.sendto(msg.encode("utf-8"),clientsocket.getsockname())

socketserver.close()
