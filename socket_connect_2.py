import socket

socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP宣告

socket2.connect(("172.20.10.11",9487))

msg = input("please enter your message : ")

socket2.send(msg.encode())
socket2.send("123213".encode())