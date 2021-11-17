class Register:

    def __init__(self, rq, name, ip_address, udp_socket, tcp_socket, **_):
        self.TYPE = "REGISTER"
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


class Registered:

    def __init__(self, rq, **_):
        self.TYPE = "REGISTERED"
        self.rq = rq

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq} 
        """


class RegisterDenied:

    def __init__(self, rq, reason, **_):
        self.TYPE = "REGISTER-DENIED"
        self.rq = rq
        self.reason = reason

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        REASON:\t{self.reason}
        """


class DeRegister:

    def __init__(self, rq, name, **_):
        self.TYPE = "DE-REGISTER"
        self.rq = rq
        self.name = name

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        NAME:\t{self.name}
        """
