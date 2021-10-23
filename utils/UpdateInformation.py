class UpdateContact:
    def __init__(self, rq, name, ip_address, udp_socket, tcp_socket):
        self.rq = rq
        self.name = name
        self.ip_address = ip_address
        self.udp_socket = udp_socket
        self.tcp_socket = tcp_socket

    def __str__(self):
        return f"""
    UPDATE CONTACT
        RQ:\t\t{self.rq}
        NAME:\t{self.name}
        IP:\t\t{self.ip_address}
        UDP:\t{self.udp_socket} 
        TCP:\t{self.tcp_socket}
        """


class UpdateConfirmed:
    def __init__(self, rq, name, ip_address, udp_socket, tcp_socket):
        self.rq = rq
        self.name = name
        self.ip_address = ip_address
        self.udp_socket = udp_socket
        self.tcp_socket = tcp_socket

    def __str__(self):
        return f"""
    UPDATE CONFIRMED
        RQ:\t\t{self.rq}
        NAME:\t{self.name}
        IP:\t\t{self.ip_address}
        UDP:\t{self.udp_socket} 
        TCP:\t{self.tcp_socket}
        """


class UpdateDenied:
    def __init__(self, rq, name, reason):
        self.rq = rq
        self.name = name
        self.reason = reason

    def __str__(self):
        return f"""
    UPDATE DENIED
        RQ:\t\t{self.rq}
        NAME:\t{self.name}
        REASON:\t{self.reason}
        """
