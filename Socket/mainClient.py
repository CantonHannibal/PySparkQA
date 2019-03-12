import socket

client = socket.socket()


host ='127.0.0.1'

port = 9092

client.connect((host, port))

while True:

    sendmsg = input("input:")

    if sendmsg=='q':
        break

    sendmsg = sendmsg

    client.sendto(sendmsg.encode("utf-8"),(host,port))
    msg = client.recv(1024)

    print(msg.decode("utf-8"))

# client.close()
