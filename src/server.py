import socket
address = ('localhost', 8000)
BUFFSIZE = 16
server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_sock.bind(address)

while True:
    msg, addr = server_sock.recvfrom(BUFFSIZE)
    print(msg.decode())