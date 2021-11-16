class ClientData:

    def __init__(self, name, ip_address, udp_socket, tcp_socket, **_):
        self.rq = None
        self.name = name
        self.ip_address = ip_address
        self.udp_socket = udp_socket
        self.tcp_socket = tcp_socket
        self.list_of_available_files = []

    def __str__(self):
        return """\
    CLIENT DATA
        RQ:\t{self.rq}
        NAME:\t{self.name}
        IP:\t{self.ip_address}
        UDP:\t{self.udp_socket} 
        TCP:\t{self.tcp_socket}
        LIST OF AVAILABLE FILES:\t{self.list_of_available_files}
        """

    def to_csv_row(self):
        return [self.rq, self.name, self.ip_address, self.udp_socket, self.tcp_socket]

class ClientInfo:

    def __init__(self, name, ip_address, tcp_socket, list_of_available_files, **_):
        self.rq = None
        self.name = name
        self.ip_address = ip_address
        self.tcp_socket = tcp_socket
        self.list_of_available_files = list_of_available_files

    def __str__(self):
        return """\
    CLIENT DATA
        RQ:\t{self.rq}
        NAME:\t{self.name}
        IP:\t{self.ip_address}
        TCP:\t{self.tcp_socket}
        LIST OF AVAILABLE FILES:\t{self.list_of_available_files}
        """

    def to_csv_row(self):
        return [self.rq, self.name, self.ip_address, self.tcp_socket]

class FileOwner:

    def __init__(self, name, ip_address, tcp_socket, **_):
        self.rq = None
        self.name = name
        self.ip_address = ip_address
        self.tcp_socket = tcp_socket

    def __str__(self):
        return """\
    CLIENT DATA
        RQ:\t{self.rq}
        NAME:\t{self.name}
        IP:\t{self.ip_address}
        TCP:\t{self.tcp_socket}
        """

    def to_csv_row(self):
        return [self.rq, self.name, self.ip_address, self.tcp_socket]

