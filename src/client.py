import socket
address = ('localhost', 8000)
client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = input("Ingrese un mensaje piola: ")
print("Enviando...")
client_sock.sendto(data.encode(), address)
print("Enviado!")

