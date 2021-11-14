import os
import socket
from threading import Thread
from Utils.Registration import Register, Registered, RegisterDenied, DeRegister
from Utils.UtilityFunctions import *
from Utils.Publishing import Publish, Published, PublishDenied, Remove, RemoveDenied, Removed
from Utils.UpdateInformation import UpdateDenied, UpdateConfirmed, UpdateContact
BUFFER_SIZE = 1024


class Client:
    UDP_PORT = 8080
    SERVER_ADDRESS = ("127.0.0.1", 8000)

    def __init__(self):
        super().__init__()
        self.tcp_socket = "tcp_socket"
        self.rq = None
        self.name = None
        self.list_of_available_files = []
        self.get_list_of_available_files()
        self.ip_address = socket.gethostbyname(socket.gethostname())
        self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udp_socket.bind((self.ip_address, self.UDP_PORT))
        self.udp_socket.settimeout(3)
        print("Client Live: " + str(self.udp_socket))

    def send_message_to_server(self, message):
        bytes_to_send = object_to_bytes(message)
        self.udp_socket.sendto(bytes_to_send, self.SERVER_ADDRESS)

    def get_list_of_available_files(self):
        current_directory = os.getcwd()
        path = 'ClientFiles'
        os.chdir(path)
        files = os.listdir()
        for i in files:
            self.list_of_available_files.append(i)
        os.chdir(current_directory)

    def __del__(self):
        self.udp_socket.close()


class RegisterWithServer(Thread):

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.server_response = None
        self.result = None
        self.response_messages = {
            "REGISTERED": self.registered,
            "REGISTER-DENIED": self.register_denied
        }

    def run(self):
        register = Register(self.client.name, self.client.ip_address, self.client.udp_socket.getsockname()[1],
                            "TCP SOCKET")
        self.client.send_message_to_server(register)

        try:
            self.server_response = self.client.udp_socket.recvfrom(BUFFER_SIZE)
            self.result = self.response_messages[get_message_type(self.server_response[0])]()
        except socket.error:
            self.result = "Connection to Server timed out."

    def join(self, *args, **kwargs):
        super().join()
        return self.result

    def registered(self):
        registered = Registered(**bytes_to_object(self.server_response[0]))
        self.client.rq = registered.rq
        log(registered)
        return True

    def register_denied(self):
        register_denied = RegisterDenied(**bytes_to_object(self.server_response[0]))
        log(register_denied)
        return register_denied.reason


class DeRegisterFromServer(Thread):

    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        de_register = DeRegister(self.client.rq, self.client.name)
        self.client.send_message_to_server(de_register)
        log(de_register)


class PublishFilesToServer(Thread):

    def __init__(self, client, list_of_files_to_publish):
        super().__init__()
        self.client = client
        self.server_response = None
        self.list_of_files_to_publish = list_of_files_to_publish
        self.result = None
        self.response_messages = {
            "PUBLISHED": self.published,
            "PUBLISH-DENIED": self.publish_denied
        }

    def run(self):
        publish = Publish(self.client.rq, self.client.name, self.list_of_files_to_publish)
        self.client.send_message_to_server(publish)

        try:
            self.server_response = self.client.udp_socket.recvfrom(BUFFER_SIZE)
            self.result = self.response_messages[get_message_type(self.server_response[0])]()
        except socket.error:
            self.result = "Connection Timed Out"

    def join(self, *args, **kwargs):
        super().join()
        return self.result

    def published(self):
        # NOT SURE ABOUT THIS NEXT LINE
        published = Published(**bytes_to_object(self.server_response[0]))
        log(published)
        return True

    def publish_denied(self):
        # NOT SURE ABOUT THIS NEXT LINE
        publish_denied = PublishDenied(**bytes_to_object(self.server_response[0]))
        log(publish_denied)
        return publish_denied.reason


class RemoveFilesFromServer(Thread):
    def __init__(self, client, list_of_files_to_remove):
        super().__init__()
        self.client = client
        self.list_of_files_to_remove = list_of_files_to_remove
        self.server_response = None
        self.result = None
        self.response_messages = {
            "REMOVED": self.removed,
            "REMOVE-DENIED": self.remove_denied
        }

    def run(self):
        remove = Remove(self.client.rq, self.client.name, self.list_of_files_to_remove)
        self.client.send_message_to_server(remove)
        try:
            self.server_response = self.client.udp_socket.recvfrom(BUFFER_SIZE)
            self.result = self.response_messages[get_message_type(self.server_response[0])]()
        except socket.error:
            self.result = "Connection Timed Out"

    def join(self, *args, **kwargs):
        super().join()
        return self.result

    def removed(self):
        removed = Removed(**bytes_to_object(self.server_response[0]))
        log(removed)
        return True

    def remove_denied(self):
        remove_denied = RemoveDenied(**bytes_to_object(self.server_response[0]))
        log(remove_denied)
        return remove_denied.reason


class UpdateClientContact(Thread):

    def __init__(self, client, new_ip, new_udp_socket, new_tcp_socket):
        super().__init__()
        self.client = client
        self.new_ip = new_ip
        self.new_udp_socket = new_udp_socket
        self.new_tcp_socket = new_tcp_socket
        self.server_response = None
        self.result = None
        self.response_messages = {
            "UPDATE-CONFIRMED": self.update_confirmed,
            "UPDATE-DENIED": self.update_denied
        }

    def run(self):
        update_contact = UpdateContact(self.client.rq, self.client.name, self.new_ip, self.new_udp_socket, self.new_tcp_socket)
        self.client.send_message_to_server(update_contact)
        try:
            self.server_response = self.client.udp_socket.recvfrom(BUFFER_SIZE)
            self.result = self.response_messages[get_message_type(self.server_response[0])]()
        except socket.error:
            self.result = "Connection Timed Out"

    def join(self, *args, **kwargs):
        super().join()
        return self.result

    def update_confirmed(self):
        update_confirmed = UpdateConfirmed(**bytes_to_object(self.server_response[0]))
        log(update_confirmed)
        return True

    def update_denied(self):
        update_denied = UpdateDenied(**bytes_to_object(self.server_response[0]))
        log(update_denied)
        return update_denied.reason


client = Client()
list = ['Test.txt']
client.name = "Joe"
d = RegisterWithServer(client)
d.start()
d.join()
#p = PublishFilesToServer(client, list)
#p.start()
#p.join()
#r = RemoveFilesFromServer(client, list)
#r.start()
#r.join()
new_ip = "192.169.101"
new_udp_socket = 8000
new_tcp_socket = "HELLO CHANGED"
u = UpdateClientContact(client, new_ip, new_udp_socket, new_tcp_socket)
u.start()
u.join()
