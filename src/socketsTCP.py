import socket
SPACER_DELIMITER = '|||'

class SocketTCP():
    def __init__(self):
        self.dest_address: tuple[str, int] = ('localhost', 8000)
        self.origin_address: tuple[str, int] = ('localhost', 8000)
        self.sequence_number: int = 0
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    @staticmethod
    def parse_segment(segment_tcp: str):
        """Paresea segmentos tcp a un diccionario de python son los siguientes campos
        ACK -> es el acknoledge de el mensaje
        SYN -> ....
        FIN ->
        SEQ -> es el numero de sequencia
        DATA -> son los datos a enviar
        """
        data = segment_tcp.split(SPACER_DELIMITER)

    @staticmethod
    def create_segment(data_dict: dict):
        """Crea un segmento de datos tcp a partir de un diccionario de python"""
        ...