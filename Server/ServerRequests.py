from threading import Thread
from ClientDatabase import Database
from ClientData import ClientData
from Utils.Registration import Register, Registered, RegisterDenied, DeRegister
from Utils.UtilityFunctions import *


class ServerRequestHandler(Thread):

    def __init__(self, bytes_received, client_list, udp_socket):
        super().__init__()
        self.client_list = client_list
        self.data = bytes_to_object(bytes_received[0])
        self.message_type = get_message_type(bytes_received[0])
        self.client_ip_address = bytes_received[1]
        self.udp_socket = udp_socket
        self.client_database = Database()
        self.request_types = {
            "REGISTER": self.register,
            "DE-REGISTER": self.de_register
        }

    def run(self):
        self.request_types[self.message_type]()

    def send_message_to_client(self, message):
        bytes_to_send = object_to_bytes(message)
        self.udp_socket.sendto(bytes_to_send, self.client_ip_address)

    def register(self):
        register = Register(**self.data)
        log(register)

        client = ClientData(**register.__dict__)
        client.rq = len(self.client_list)

        if any(client.name == c.name for c in self.client_list):
            register_denied = RegisterDenied(client.rq, "Client with same name already registered!")
            log(register_denied)
            self.send_message_to_client(register_denied)
        else:
            self.client_list.append(client)
            self.client_database.register_client(client)

            registered = Registered(client.rq)
            self.send_message_to_client(registered)
            log(registered)

    def de_register(self):
        de_register = DeRegister(**self.data)
        # TODO de register by name; RQ is per request
        self.client_list = [client for client in self.client_list if client.rq != de_register.rq]
        self.client_database.de_register_client(de_register.rq)
        log(de_register)

    def publish(self):
        print()
        # add list of available files to client with RQ

