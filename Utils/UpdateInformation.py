class UpdateContact:

    def __init__(self, rq, name, ip_address, udp_socket, tcp_socket, **_):
        self.TYPE = "UPDATE-CONTACT"
        self.rq = rq
        self.name = name
        self.ip_address = ip_address
        self.udp_socket = udp_socket
        self.tcp_socket = tcp_socket

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        NAME:\t{self.name}
        IP:\t{self.ip_address}
        UDP:\t{self.udp_socket} 
        TCP:\t{self.tcp_socket}
        """


class UpdateConfirmed:

    def __init__(self, rq, name, ip_address, udp_socket, tcp_socket, **_):
        self.TYPE = "UPDATE-CONFIRMED"
        self.rq = rq
        self.name = name
        self.ip_address = ip_address
        self.udp_socket = udp_socket
        self.tcp_socket = tcp_socket

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        NAME:\t{self.name}
        IP:\t{self.ip_address}
        UDP:\t{self.udp_socket} 
        TCP:\t{self.tcp_socket}
        """


class UpdateDenied:

    def __init__(self, rq, name, reason, **_):
        self.TYPE = "UPDATE-DENIED"
        self.rq = rq
        self.name = name
        self.reason = reason

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        NAME:\t{self.name}
        REASON:\t{self.reason}
        """
