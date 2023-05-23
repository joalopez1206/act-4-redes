import socket

SPACER_DELIMITER = '|||'
HEADERS = SYN, ACK, FIN, SEQ, DATA = 'SYN', 'ACK', 'FIN', 'SEQ', 'DATA'


class SocketTCP():
    def __init__(self):
        self.dest_address: tuple[str, int] = ('localhost', 8000)
        self.origin_address: tuple[str, int] = ('localhost', 8000)
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
    def create_segment(data_dict: dict) -> str:
        """Crea un segmento de datos tcp a partir de un diccionario de python"""
        retstr: str = '|||'
        retstr = retstr.join([data_dict[value] for value in HEADERS])
        return retstr


if __name__ == '__main__':
    print(SocketTCP.create_segment(
        SocketTCP.parse_segment('0|||0|||0|||98|||Mensaje de prueba')
    ))
