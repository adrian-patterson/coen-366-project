import json
import threading
from ClientDatabase import Database
from Utils.Registration import Register, Registered
from ClientData import ClientData
from Utils.UtilityFunctions import object_to_bytes, bytes_to_object


class ClientRequestHandler(threading.Thread):

    def __init__(self, bytes_received, client_list, udp_socket):
        super().__init__()
        self.client_list = client_list
        self.client_database = Database()
        self.data = bytes_to_object(bytes_received[0])
        self.client_ip_address = bytes_received[1]
        self.message_type = json.loads(bytes_received[0])["TYPE"]
        self.udp_socket = udp_socket
        self.request_types = {
            "REGISTER": self.register_client
        }

    def run(self):
        self.request_types[self.message_type]()

    def register_client(self):
        register = Register(**self.data)
        client = ClientData(**register.__dict__)

        client.rq = len(self.client_list)
        self.client_list.append(client)
        self.client_database.register_client(client)

        registered = Registered(client.rq)
        bytes_to_send = object_to_bytes(registered)
        self.udp_socket.sendto(bytes_to_send, self.client_ip_address)

