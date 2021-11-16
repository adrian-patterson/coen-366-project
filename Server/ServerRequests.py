from threading import Thread
from ClientDatabase import Database
from ClientData import ClientData
from Utils.FileTransfer import Download, DownloadError
from Utils.Registration import Register, Registered, RegisterDenied, DeRegister
from Utils.UtilityFunctions import *
from Utils.Publishing import Publish, Published, PublishDenied, Remove, RemoveDenied, Removed
from Utils.Retrieve import RetrieveAll, Retrieve, RetrieveError, RetrieveInfoRequest, RetrieveInfoResponse, SearchError, SearchFileRequest, SearchFileResponse


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
            "DE-REGISTER": self.de_register,
            "PUBLISH": self.publish,
            "REMOVE": self.remove,
            "RETRIEVE-ALL": self.retrieve_all,
            "RETRIEVE-INFOT": self.retrieve_infot,
            "SEARCH-FILE": self.search_file
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
        publish = Publish(**self.data)
        log(publish)
        client_exist = False
        for client in self.client_list:
            if client.name == publish.name:
                client_exist = True
                for file in publish.list_of_files:
                    if file not in client.list_of_available_files:
                        client.list_of_available_files.append(file)

        if client_exist:
            published = Published(publish.rq)
            self.send_message_to_client(published)
            log(published)
        else:
            publish_denied = PublishDenied(publish.rq, "Client " + publish.name + " is not registered")
            self.send_message_to_client(publish_denied)
            log(publish_denied)

    def remove(self):
        remove = Remove(**self.data)
        log(remove)
        client_exist = False
        for client in self.client_list:
            if client.name == remove.name:
                client_exist = True
                for file in remove.list_of_files_to_remove:
                    if file != remove.list_of_files_to_remove:
                        client.list_of_available_files = [file]
        if client_exist:
            removed = Removed(remove.rq)
            self.send_message_to_client(removed)
            log(removed)
        else:
            remove_denied = RemoveDenied(remove.rq, "Client " + remove.name + " is not registered")
            self.send_message_to_client(remove_denied)
            log(remove_denied)

    def retrieve_all(self):
        retireve_all = RetrieveAll(**self.data)
        log(retireve_all)
        registered_client = True
        client_info_list = []
        for client in self.client_list:
            client_info = {"name":client.name, "ip_address" : client.ip_address, 
            "tcp_socket": client.tcp_socket, "list_of_available_files":client.list_of_available_files}
            client_info_list.append(client_info)
        
        if registered_client:
            retrieve_all = Retrieve(retireve_all.rq, client_info_list)
            self.send_message_to_client(retrieve_all)
            log(retrieve_all)
        else:
            retrieve_error = RetrieveError(retireve_all.rq, "Client " + " is not registered")
            self.send_message_to_client(retrieve_error)
            log(retrieve_error)

    def retrieve_infot(self):
        retrieve_info_request = RetrieveInfoRequest(**self.data)
        log(retrieve_info_request)
        specific_client = None
        for client in self.client_list:
            if client.name == retrieve_info_request.name:
                specific_client = client

        if specific_client is not None:
            retrieve_info_response = RetrieveInfoResponse(retrieve_info_request.rq,specific_client.name 
            , specific_client.ip_address, specific_client.tcp_socket,
            specific_client.list_of_available_files)
            self.send_message_to_client(retrieve_info_response)
            log(retrieve_info_response)
        elif specific_client is None:
            retrieve_error = RetrieveError(retrieve_info_request.rq, "Client " +
             " is not registered")
            self.send_message_to_client(retrieve_error)
            log(retrieve_error)
        else:
            retrieve_error = RetrieveError(retrieve_info_request.rq, "Client " +
            retrieve_info_request.name+ " is not registered")
            self.send_message_to_client(retrieve_error)
            log(retrieve_error)

    def search_file(self):
        search_file_request = SearchFileRequest(**self.data)
        log(search_file_request)
        file_owner_list = None
        for client in self.client_list:
            if (search_file_request.file_name not in client.list_of_available_files):
                continue
            file_owner = {"name" :client.name, "ip_address" :client.ip_address, "tcp_socket" : client.tcp_socket}
            file_owner_list.append(file_owner)

        if file_owner_list is not None:
            search_file_response = SearchFileResponse(search_file_request.rq, file_owner_list)
            self.send_message_to_client(search_file_response)
            log(search_file_response)
        elif file_owner_list is None:
            search_error = SearchError(search_file_request.rq, "Client " +
             " is not registered")
            self.send_message_to_client(search_error)
            log(search_error)
        else:
            search_error = SearchError(search_file_request.rq, "Client " +
            search_file_request.file+ " is not published")
            self.send_message_to_client(search_error)
            log(search_error)

    