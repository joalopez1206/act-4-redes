import socket
from SocketTCP import SocketTCP
address = ('localhost', 8000)
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = input("Ingrese un mensaje piola: ")


# mensaje definido mayor a 16 chars

def sendfullmsg(sender_sock: socket.socket, msg: bytes, addr: tuple[str, int], buff_size=16):
    largo_mensaje: int = len(msg)
    byte_inicial = 0
    msg_sent_so_far = ''.encode()
    while msg_sent_so_far != msg:
        max_byte = min(largo_mensaje, byte_inicial + buff_size)
        message_slice = msg[byte_inicial: max_byte]
        alo = sender_sock.sendto(message_slice, addr)
        print(alo)
        msg_sent_so_far += message_slice
        byte_inicial += alo
    return


print("Sending...")
sendfullmsg(client_sock, data.encode(), address)
print("Sent!")
