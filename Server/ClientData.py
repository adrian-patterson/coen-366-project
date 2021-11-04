

class ClientData:

    def __init__(self, name, ip_address, udp_socket, tcp_socket, **_):
        self.rq = None
        self.name = name
        self.ip_address = ip_address
        self.udp_socket = udp_socket
        self.tcp_socket = tcp_socket
        self.list_of_available_files = []

    def to_csv_row(self):
        return [self.rq, self.name, self.ip_address, self.udp_socket]
