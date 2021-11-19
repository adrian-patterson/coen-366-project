import os
import socket
from threading import Thread
from Utils.Registration import Register, Registered, RegisterDenied, DeRegister
from Utils.UtilityFunctions import *
from Utils.Publishing import Publish, Published, PublishDenied, Remove, RemoveDenied, Removed
from Utils.Retrieve import RetrieveAll, Retrieve, RetrieveError, RetrieveInfoRequest, RetrieveInfoResponse, SearchError, SearchFileRequest, SearchFileResponse

BUFFER_SIZE = 1024


class Client:
    UDP_PORT = 8000
    SERVER_ADDRESS = ('192.168.169.2',8090)

    def __init__(self):
        super().__init__()
        self.rq = None
        self.name = None
        self.list_of_available_files = []
        self.get_list_of_available_files()
        self.ip_address = socket.gethostbyname(socket.gethostname())
        self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.udp_socket.bind((self.ip_address, self.UDP_PORT))
        self.udp_socket.settimeout(3)
        self.tcp_socket = None
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

    def increment_rq(self):
        self.rq += 1

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
        register = Register(self.client.rq, self.client.name, self.client.ip_address, self.client.udp_socket.getsockname()[1],
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

    def __init__(self, client,list_of_files_to_publish):
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
    def __init__(self, client,list_of_files_to_remove):
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

class RetrieveAllClientsFromServer(Thread):

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.server_response = None
        self.result = None
        self.response_messages = {
            "RETRIEVE": self.retrieve,
            "RETRIEVE_ERROR": self.retrieve_error
        }

    def run(self):
        retrieve_all = RetrieveAll(self.client.rq)
        self.client.send_message_to_server(retrieve_all)

        try:
            self.server_response = self.client.udp_socket.recvfrom(BUFFER_SIZE)
            self.result = self.response_messages[get_message_type(self.server_response[0])]()
        except socket.error:
            self.result = "Connection Timed Out"

    def join(self, *args, **kwargs):
        super().join()
        return self.result

    def retrieve(self):
        retrieve = Retrieve(**bytes_to_object(self.server_response[0]))
        log(retrieve)
        return True

    def retrieve_error(self):
        retrieve_error = RetrieveError(**bytes_to_object(self.server_response[0]))
        log(retrieve_error)
        return retrieve_error.reason


class RetrieveClientInfoFromServer(Thread):

    def __init__(self, client, name):
        super().__init__()
        self.client = client
        self.server_response = None
        self.name = name
        self.result = None
        self.response_messages = {
            "RETRIEVE-INFOT": self.retrieve_infot,
            "RETRIEVE-ERROR": self.retrieve_error
        }

    def run(self):
        retrieve_info_request = RetrieveInfoRequest(self.client.rq, self.name)
        self.client.send_message_to_server(retrieve_info_request)

        try:
            self.server_response = self.client.udp_socket.recvfrom(BUFFER_SIZE)
            self.result = self.response_messages[get_message_type(self.server_response[0])]()
        except socket.error:
            self.result = "Connection Timed Out"

    def join(self, *args, **kwargs):
        super().join()
        return self.result

    def retrieve_infot(self):
        retrieve_info_response = RetrieveInfoResponse(**bytes_to_object(self.server_response[0]))
        log(retrieve_info_response)
        return True

    def retrieve_error(self):
        retrieve_error = RetrieveError(**bytes_to_object(self.server_response[0]))
        log(retrieve_error)
        return retrieve_error.reason


class SearchFileFromDataBase(Thread):

    def __init__(self, client, file_name):
        super().__init__()
        self.client = client
        self.server_response = None
        self.file_name = file_name
        self.result = None
        self.response_messages = {
            "SEARCH-FILE": self.search_file,
            "SEARCH-ERROR": self.search_error
        }

    def run(self):
        search_file_request = SearchFileRequest(self.client.rq, self.file_name)
        self.client.send_message_to_server(search_file_request)

        try:
            self.server_response = self.client.udp_socket.recvfrom(BUFFER_SIZE)
            self.result = self.response_messages[get_message_type(self.server_response[0])]()
        except socket.error:
            self.result = "Connection Timed Out"

    def join(self, *args, **kwargs):
        super().join()
        return self.result

    def search_file(self):
        search_file_response = SearchFileResponse(**bytes_to_object(self.server_response[0]))
        log(search_file_response)
        return True

    def search_error(self):
        search_error = SearchError(**bytes_to_object(self.server_response[0]))
        log(search_error)
        return search_error.reason



client = Client()
client.name = "Jin"
client.rq = 5

# client2 = Client()
# client2.name = "Jin"
# client2.rq = 5

print(client.name)
register_thread = PublishFilesToServer(client,['hello2.txt', "hi.txt"])
# register_thread = RegisterWithServer(client)
# register_thread = RetrieveAllClientsFromServer(client)
# register_thread = SearchFileFromDataBase(client, '  hello.txt')
# register_thread = RemoveFilesFromServer(client, ['hi.txt'])
register_thread.start()
register_thread.join()


