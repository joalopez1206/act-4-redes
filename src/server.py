import socket

address = ('localhost', 8000)
BUFFSIZE = 16
server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_sock.bind(address)


def recvfullmsg(receiver_socket, size) -> bytes:
    while True:
        msg, _ = receiver_socket.recvfrom(size)
        print(msg.decode())
    return msg


while True:
    recvfullmsg(server_sock, BUFFSIZE)
