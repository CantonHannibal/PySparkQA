import socket

sk1 = socket.socket()  # sk1,sk2,sk3这就是一个文件描述符
sk1.bind(('127.0.0.1', 8002))
sk1.listen()

#
# sk2 = socket.socket()
# sk2.bind(('127.0.0.1',8003))
# sk2.listen()
#
# sk3 = socket.socket()
# sk3.bind(('127.0.0.1',8004))
# sk3.listen()

inputs = [sk1]
import select

# epoll效率更高，但是Windows不支持，它是谁有问题就告诉它，不用循坏
while True:
    '''[sk1,sk2,sk3],select内部会自动监听sk1,sk21，sk3三个对象
    一旦某个句柄发生变化（某人来链接）就会被监听到
    '''
    # 如果有人链接sk1，则会被添加进列表，r_list = [sk1]
    r_list, w_list, e_list = select.select(inputs, [], [], 1)
    '''第三个参数是监听错误的，只要有错误出现，就会被监听到，返回e_list
       第二个参数返回给w_list，只要传了什么，就原封不动的传给w_list'''
    print('正在监听 %s 多少个对象' % len(inputs))
    for sk in r_list:
        if sk == sk1:
            # 句柄跟服务器端的对象一样，表示有新用户来链接了
            conn, address = sk.accept()
            # conn.sendall(bytes('你好', encoding='utf-8'))
            inputs.append(conn)  # 加入去之后，inputs有一个链接对象和服务器对象
            # conn.sendall(bytes('你好', encoding='utf-8'))
        else:
            # 有老用户发消息了
            try:
                data_byte = sk.recv(1024)
                print('Server has been recieved!')
                data_str = str(data_byte, encoding='utf-8')
                sk.sendall(bytes(data_str + '收到了', encoding='utf-8'))
                print('Server has been sent')
            except:  # 空信息表示客户端断开链接，所以要在监听中移除

                inputs.remove(sk)  # 这里的sk就是之前传进去的conn，因为r_list接收的是有变化的值