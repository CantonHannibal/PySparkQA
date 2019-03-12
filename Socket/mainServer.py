from socket import *
import threading
import time

conn_list = []
conn_dt = {}
# clientsocket,addr = socketserver.accept()

def tcplink(sock:socket,addr):
    print('Accept new connection from %s:%s...' % addr)
    # sock.send(b'Welcome!')
    while True:
        try:
            recvmsg = sock.recv(1024)
            strData = recvmsg.decode("utf-8")
            print(addr + " Roger:" + strData)
            # time.sleep(1)
            if  strData == 'q':
                break
            # msg = input("reply:")
            # socketserver.send(data=msg.encode("utf-8"))
            # socketserver.sendto(data=msg.encode("utf-8"),args=sock.getsockname())
            # sock.close()
        except:
            sock.close()
            print(addr,'offline')
            _index = conn_list.index(addr)
            conn_dt.pop(addr)
            conn_list.pop(_index)
            break
    # socketserver.close()
def recs():
    socketserver = socket()
    host = '0.0.0.0'
    port = 9092

    socketserver.bind((host, port))
    socketserver.listen(5)
    print("Waiting for connection...")
    while True:
        clientsock, clientaddress = socketserver.accept()
        # print("yyyyyy",clientsock, clientaddress,"yyyy")
        if clientaddress not in conn_list:
            conn_list.append(clientaddress)
            conn_dt[clientaddress] = clientsock
            # gui.listBox.insert(END, clientaddress)
        print('connect from:', clientaddress)
        # 在这里创建线程，就可以每次都将socket进行保持
        t = threading.Thread(target=tcplink, args=(clientsock, clientaddress))
        t.start()

if __name__ == '__main__':
    recs()

    # recvmsg = clientsocket.recv(1024)










socketserver.close()
