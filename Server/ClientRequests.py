import json
import threading
from Utils.ClientDatabase import Database
from Utils.Registration import Register
from ClientData import ClientData


class ClientRequestHandler(threading.Thread):

    def __init__(self, bytes_received, client_list):
        super().__init__()
        self.client_list = client_list
        self.client_database = Database()
        self.json_data = json.loads(bytes_received[0])
        self.message_type = self.json_data["TYPE"]
        self.request_types = {
            "REGISTER": self.register_client
        }

    def run(self):
        self.request_types[self.message_type]()

    def register_client(self):
        register = Register(**self.json_data)
        client = ClientData(**register.__dict__)
        client.rq = len(self.client_list)
        self.client_list.append(client)
        self.client_database.register_client(client)

