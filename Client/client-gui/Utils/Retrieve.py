class RetrieveAll:

    def __init__(self, rq, **_):
        self.TYPE = "RETRIEVE-ALL"
        self.rq = rq

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        """


class Retrieve:

    def __init__(self, rq, list_of_clients, **_):
        self.TYPE = "RETRIEVE"
        self.rq = rq
        self.list_of_clients = list_of_clients

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        LIST OF CLIENTS:\t{self.list_of_clients}
        """


class RetrieveInfoRequest:

    def __init__(self, rq, name, **_):
        self.TYPE = "RETRIEVE-INFO-REQUEST"
        self.rq = rq
        self.name = name

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        NAME:\t{self.name}
        """


class RetrieveInfoResponse:

    def __init__(self, rq, name, ip_address, tcp_socket, list_of_available_files, **_):
        self.TYPE = "RETRIEVE-INFO-RESPONSE"
        self.rq = rq
        self.name = name
        self.ip_address = ip_address
        self.tcp_socket = tcp_socket
        self.list_of_available_files = list_of_available_files

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        NAME:\t{self.name}
        IP:\t{self.ip_address}
        TCP:\t{self.tcp_socket}
        LIST OF AVAILABLE FILES:\t{self.list_of_available_files}
        """


class RetrieveError:

    def __init__(self, rq, reason, **_):
        self.TYPE = "RETRIEVE-ERROR"
        self.rq = rq
        self.reason = reason

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        REASON:\t{self.reason}
        """


class SearchFileRequest:

    def __init__(self, rq, file_name, **_):
        self.TYPE = "SEARCH-FILE-REQUEST"
        self.rq = rq
        self.file_name = file_name

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        FILE NAME:\t{self.file_name}
        """


class SearchFileResponse:

    def __init__(self, rq, list_of_clients, **_):
        self.TYPE = "SEARCH-FILE-RESPONSE"
        self.rq = rq
        self.list_of_clients = list_of_clients

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        LIST OF CLIENTS:\t{self.list_of_clients}
        """


class SearchError:

    def __init__(self, rq, reason, **_):
        self.TYPE = "SEARCH-ERROR"
        self.rq = rq
        self.reason = reason

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        REASON:\t{self.reason}
        """
