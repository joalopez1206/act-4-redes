import random
import socket

SPACER_DELIMITER = '|||'
HEADERS = SYN, ACK, FIN, SEQ, DATA = 'SYN', 'ACK', 'FIN', 'SEQ', 'DATA'


class SocketTCP():
    def __init__(self, dest_address: tuple[str, int] = ('localhost', 8000),
                 origin_address: tuple[str, int] = ('localhost', 8000)):
        self.dest_address: tuple[str, int] = dest_address
        self.origin_address: tuple[str, int] = origin_address
        self.sequence_number: int = 0
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

    @staticmethod
    def create_segment_from_dict(data_dict: dict) -> str:
        """Crea un segmento de datos tcp a partir de un diccionario de python"""
        retstr: str = '|||'
        retstr = retstr.join([data_dict[value] for value in HEADERS])
        return retstr

    @staticmethod
    def create_segment(syn, ack, fin, seq, data) -> str:
        return SocketTCP.create_segment_from_dict({ACK: ack, SYN: syn, FIN: fin, SEQ: seq, DATA: data})

    def syn_msg(self):
        return SocketTCP.create_segment('1', 0, 0, self.sequence_number, '')

    @staticmethod
    def tostr_segment(data_dict: dict) -> str:
        return str(data_dict)

    def bind(self, address: tuple[str, int]):
        self.origin_address = address
        self.socket.bind(self.origin_address)

    def connect(self, address: tuple[str, int]):
        # Seteamos la direccion a conectar igual al address y creamos un numero de secuencia al azar
        self.dest_address = address
        self.sequence_number = random.randint(0, 100)

        # ahora vamos a hacer el primer handshake
        # lo primero es TIRAR un SYN y ver que pasa
        syn_msg = self.syn_msg()
        self.socket.sendto(syn_msg.encode(), self.dest_address)

        # luego estamos atento a recibir el mensaje de los headers
        syn_ack_msg_recv, _ = self.socket.recvfrom(19)

        # recivimos el mensaje y ahora le mandamos un syn_ack (suponemos que lo envia bien! o sea hay que checkear)
        parse_msg = SocketTCP.parse_segment(syn_ack_msg_recv.decode())
        # actualizamos el sequence number
        self.sequence_number = int(parse_msg[SEQ])
        # y ahora enviamos un ack y terminamos!
        ack_msg = self.ack_msg()
        self.socket.sendto(ack_msg.encode(), self.dest_address)

    def ack_msg(self):
        self.sequence_number += 1
        return SocketTCP.create_segment('0', '1', '0', self.sequence_number, '')

    def accept(self):
        msg, self.dest_address = self.socket.recvfrom(19)
        headers = SocketTCP.parse_segment(msg.decode())
        #Espero que llegue un SYN
        while headers["SYN"] != 0:
            msg, _ = self.socket.recvfrom(19)
            headers = SocketTCP.parse_segment(msg.decode())
        self.sequence_number+=1
        #cuando llegue entonces mensajeo un SYN+ACK y suma a la secuencia!
        msg_to_send = SocketTCP.create_segment('1','1','0',f'{self.sequence_number}','')
        self.socket.sendto(msg_to_send)
        #Espero ahora que llegue un ACK

        msg, self.dest_address = self.socket.recvfrom(19)
        headers = SocketTCP.parse_segment(msg.decode())
        # Espero que llegue un SYN
        while headers["ACK"] != 0:
            msg, _ = self.socket.recvfrom(19)
            headers = SocketTCP.parse_segment(msg.decode())



if __name__ == '__main__':
    print(SocketTCP.create_segment_from_dict(
        SocketTCP.parse_segment(SocketTCP.create_segment('0','0','0','98','Mensaje de Prueba'))
    ))
