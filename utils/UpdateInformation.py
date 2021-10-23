class UpdateContact:
    def __init__(self, rq, name, ip_address, udp_socket, tcp_socket):
        self.rq = rq
        self.name = name
        self.ipAddress = ip_address
        self.udpSocket = udp_socket
        self.tcpSocket = tcp_socket


class UpdateConfirmed:
    def __init__(self, rq, name, ip_address, udp_socket, tcp_socket):
        self.rq = rq
        self.name = name
        self.ipAddress = ip_address
        self.udpSocket = udp_socket
        self.tcpSocket = tcp_socket


class UpdateDenied:
    def __init__(self, rq, name, reason):
        self.rq = rq
        self.name = name
        self.reason = reason
