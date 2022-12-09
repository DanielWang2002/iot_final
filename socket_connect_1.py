import socket

socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP宣告
socket1.bind(("172.20.10.11",9487))

socket1.listen(1)

def foo(recevent):
    while True:
        # print(client_addr)
        recevent = connect_socket.recv(1024)
        if str(recevent,encoding='utf-8') == 'close':
            break
        print(str(recevent,encoding='utf-8'))

connect_socket,client_addr = socket1.accept()
while True:
    recevent = connect_socket.recv(1024)
    if str(recevent,encoding='utf-8') == 'open':
        foo(recevent)
        connect_socket,client_addr = socket1.accept()
