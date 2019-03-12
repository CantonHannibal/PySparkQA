import socket

sk1 = socket.socket()  # sk1,sk2,sk3这就是一个文件描述符
sk1.bind(('127.0.0.1', 8002))
sk1.listen()

sk2 = socket.socket()
sk2.bind(('127.0.0.1', 8003))
sk2.listen()

sk3 = socket.socket()
sk3.bind(('127.0.0.1', 8004))
sk3.listen()

inputs = [sk1, sk2, sk3]
import select

while True:
    '''[sk1,sk2,sk3],select内部会自动监听sk1,sk21，sk3三个对象
    一旦某个句柄发生变化就会被监听到
    '''
    # 如果有人链接sk1，则会被添加进列表，r_list = [sk1]
    r_list, w_list, e_list = select.select(inputs, [], [], 1)  # 1表示等一秒，在while执行到这里的时候监测一秒，没有人来链接的话就接着循环
    # print(r_list,sk1.listen())
    for sk in r_list:
        conn, address = sk.accept()
        # print(conn,address)
        conn.sendall(bytes('你好', encoding='utf-8'))
        conn.close()