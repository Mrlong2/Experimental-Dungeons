import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1235))

while True:
    msg = s.recv(16)
    print(msg.decode("utf-8"))
