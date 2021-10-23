class Register:
    def __init__(self, rq, name, ip_address, udp_socket, tcp_socket):
        self.rq = rq
        self.name = name
        self.ip_address = ip_address
        self.udp_socket = udp_socket
        self.tcp_socket = tcp_socket

    def __str__(self):
        return f"""\
    REGISTER
        RQ:\t\t{self.rq}
        NAME:\t{self.name}
        IP:\t\t{self.ip_address}
        UDP:\t{self.udp_socket} 
        TCP:\t{self.tcp_socket}
        """

    def to_csv_row(self):
        return [self.rq, self.name, self.ip_address, self.udp_socket]


class Registered:
    def __init__(self, rq):
        self.rq = rq

    def __str__(self):
        return f"""
    REGISTERED
        RQ:\t\t{self.rq} 
        """


class RegisterDenied:
    def __init__(self, rq, reason):
        self.rq = rq
        self.reason = reason

    def __str__(self):
        return f"""
    REGISTER DENIED
        RQ:\t\t{self.rq}
        REASON:\t{self.reason}
        """


class DeRegister:
    def __init__(self, rq, name):
        self.rq = rq
        self.name = name

    def __str__(self):
        return f"""
    DE REGISTER
        RQ:\t\t{self.rq}
        NAME:\t{self.name}
        """
