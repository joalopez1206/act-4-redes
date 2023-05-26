from __future__ import annotations

import random
import socket

SPACER_DELIMITER = '|||'
HEADERS = SYN, ACK, FIN, SEQ, DATA = 'SYN', 'ACK', 'FIN', 'SEQ', 'DATA'
HEADERS_WITHOUT_DATA = SYN, ACK, FIN, SEQ
#vamos a definir el largo de los headers
# la idea es que la cantidad de bytes de seq sea a lo mas de 5 chars pero ocupando
# los 5 chars
# por ejemplo
# 0|||0|||0|||00231|||....
# el 00231 es para definir la cantidad del largo
# Luego el largo del header es 3*4+1+1+1+5=
HEADER_SIZE = len("0|||0|||0|||00000|||")
BUFFER_SIZE = 2**4

class SocketTCP:
    def __init__(self):
        self.dest_address: tuple[str, int] | None = None
        self.origin_address: tuple[str, int] | None = None
        self.sequence_number: int = 0
        self.sequence_number_str : str = ''
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    @staticmethod
    def parse_segment(segment_tcp: str) -> dict:
        """Parsea segmentos tcp a un diccionario de python son los siguientes campos
        ACK -> es el acknoledge de el mensaje
        SYN -> ....
        FIN ->
        SEQ -> es el numero de sequencia
        DATA -> son los datos a enviar
        """
        retdict = {}
        data = segment_tcp.split(SPACER_DELIMITER)
        for val, key in zip(data, HEADERS):
            retdict[key] = val
        return retdict

    def set_seq_number(self, num:int):
        self.sequence_number = num
        self.sequence_number_str = f"{num:05d}"
    @staticmethod
    def create_segment_from_dict(data_dict: dict) -> str:
        """Crea un segmento de datos tcp a partir de un diccionario de python"""
        retstr: str = '|||'
        retstr = retstr.join([data_dict[value] for value in HEADERS])
        return retstr

    @staticmethod
    def create_segment(syn, ack, fin, seq, data='') -> str:
        return SocketTCP.create_segment_from_dict({ACK: ack, SYN: syn, FIN: fin, SEQ: seq, DATA: data})

    def syn_msg(self):
        return SocketTCP.create_segment('1', '0', '0',self.sequence_number_str)

    @staticmethod
    def tostr_segment(data_dict: dict) -> str:
        return str(data_dict)

    def bind(self, address: tuple[str, int]):
        self.origin_address = address
        self.socket.bind(self.origin_address)

    def connect(self, address: tuple[str, int]):
        # Seteamos la direccion a conectar igual al address y creamos un numero de secuencia al azar
        self.dest_address = address
        self.set_seq_number(random.randint(0, 100))

        # ahora vamos a hacer el primer handshake
        # lo primero es TIRAR un SYN y ver que pasa
        syn_msg = self.syn_msg()
        print(f"Mensaje a enviar ---->{syn_msg}")
        self.socket.sendto(syn_msg.encode(), self.dest_address)

        # luego estamos atento a recibir el mensaje de los headers
        print("Esperando mensaje")
        syn_ack_msg_recv, self.dest_address = self.socket.recvfrom(HEADER_SIZE)

        # recibimos el mensaje y ahora le mandamos un syn_ack (suponemos que lo envia bien! o sea hay que checkear)
        parse_msg = SocketTCP.parse_segment(syn_ack_msg_recv.decode())
        while not (parse_msg.get(ACK) == '1' and parse_msg.get(SYN) == '1'):
            syn_ack_msg_recv, _ = self.socket.recvfrom(HEADER_SIZE)
            parse_msg = SocketTCP.parse_segment(syn_ack_msg_recv.decode())
        print(f"Mensaje recibido! ----> {syn_ack_msg_recv.decode()}")

        # actualizamos el sequence number
        self.set_seq_number(int(parse_msg[SEQ]) + 1)
        ack_msg = self.ack_msg()
        print(f"Mensaje a enviar ----> {ack_msg}")
        self.socket.sendto(ack_msg.encode(), self.dest_address)
        print("Mensaje Enviado!")

    def ack_msg(self):
        return SocketTCP.create_segment('0', '1', '0', self.sequence_number_str)

    def accept(self):
        # Recibimos un mensaje a ver si llega un syn
        msg, self.dest_address = self.socket.recvfrom(HEADER_SIZE)
        headers = SocketTCP.parse_segment(msg.decode())

        # Si no es SYN, entonces espero que llegue un SYN
        while headers.get("SYN") != '1':
            msg, _ = self.socket.recvfrom(HEADER_SIZE)
            headers = SocketTCP.parse_segment(msg.decode())
        print(f"Llego el mensaje SYN ----> {msg.decode()}")

        # Aumento el numero de secuencia
        self.set_seq_number(int(headers[SEQ]) + 1)

        # Y ahora lo que vamos a hacer es crear un nuevo socket con una nueva direccion
        comm_sock = SocketTCP()
        comm_sock_address = ('localhost', self.origin_address[1] + 1)
        comm_sock.set_seq_number(self.sequence_number)
        print(f"Creando socket... @{comm_sock_address}")
        comm_sock.bind(comm_sock_address)
        comm_sock.dest_address = self.dest_address

        # ¡cuando llegue entonces mensajeo un SYN+ACK y suma a la secuencia!
        msg_to_send = SocketTCP.create_segment('1', '1', '0', comm_sock.sequence_number_str)
        print(f"Enviando EL SYN+ACK ---> {msg_to_send}")
        comm_sock.socket.sendto(msg_to_send.encode(), comm_sock.dest_address)

        # Espero ahora que llegue un ACK
        print("Esperando por el ACK del cliente")
        msg, self.dest_address = comm_sock.socket.recvfrom(HEADER_SIZE)
        headers = SocketTCP.parse_segment(msg.decode())

        # Espero que llegue un ACK
        while headers.get("ACK") != '1':
            msg, _ = comm_sock.socket.recvfrom(HEADER_SIZE)
            headers = SocketTCP.parse_segment(msg.decode())
        print(f'mensaje ACK recibido! ----> {msg.decode()}')

        print("Three way handshake listo!")
        return comm_sock, comm_sock_address

    def send(self, msg: bytes):
        #Seteamos el timeout a 5 segundos
        self.socket.settimeout(5)
        # Primero enviamos el largo del mensaje en el
        # Primer segmento
        largo_msg = len(msg)
        largo_str_len_msg = len(str(largo_msg))
        segment2send = SocketTCP.create_segment('0', '0', '0', self.sequence_number_str, str(largo_msg))
        self.socket.sendto(segment2send, self.dest_address)
        recv_msg = ''
        #Ahora esperamos un ACK y verificamos que esté all good
        try:
            recv_msg, _ = self.socket.recvfrom(HEADER_SIZE)
        except TimeoutError:
            print("Trying to reach again!")
        parsed_msg = SocketTCP.parse_segment(recv_msg.decode())
        while not(parsed_msg.get("ACK") == 1):
            print("Not an ACK message!")
            try:
                msg, _ = self.socket.recvfrom(HEADER_SIZE)
            except TimeoutError:
                print("Trying to reach again!")
        self.set_seq_number(int(parsed_msg[SEQ]))

        #Ahora empezamos a transmitir los datos!
        byte_inicial = 0
        msg_sent_so_far = ''.encode()

        while msg_sent_so_far != msg:
            max_byte = min(largo_msg, byte_inicial + BUFFER_SIZE)
            message_slice = msg[byte_inicial: max_byte]
            SocketTCP.create_segment(...)

    def recv(self, buff_size):
        ...


if __name__ == '__main__':
    ...
