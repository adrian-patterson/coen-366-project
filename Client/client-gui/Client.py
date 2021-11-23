import os
from threading import Thread
from Utils.FileTransfer import File, DownloadError, Download, FileEnd
from Utils.UtilityFunctions import *

BUFFER_SIZE = 1024


# Client is a thread

class Client(Thread):
    SERVER_UDP_PORT = 5001

    def __init__(self):
        super().__init__()
        self.rq = 0
        self.name = ""
        self.list_of_available_files = []
        self.get_list_of_available_files()
        self.ip_address = get_ip_address()
        self.server_address = None
        self.udp_socket = self.udp_init()
        self.tcp_socket = self.tcp_init()
        print("Client Live:\n\t\tUDP:\t" + str(self.udp_socket) +
              "\n\t\tTCP:\t" + str(self.tcp_socket))

    # Client's TCP Socket is always listening
    def run(self):
        self.tcp_socket.listen()

        while True:
            # This represents the tcp_socket of the peer/client who wants to communicate with another client
            peer_socket = self.tcp_socket.accept()[0]
            peer_handler = Thread(
                target=self.handle_peer_request, args=(peer_socket,))
            peer_handler.start()

    # Creation of UDP Sockets to communicate with server
    def udp_init(self):
        udp_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_DGRAM)
        udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp_socket.bind((self.ip_address, 0))
        udp_socket.settimeout(3)
        return udp_socket

    # Client can generate as many tcp sockets as he wants
    def tcp_init(self):
        tcp_socket = socket.socket(
            family=socket.AF_INET, type=socket.SOCK_STREAM)
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_socket.bind((self.ip_address, 0))
        return tcp_socket

    # Function to handle Download Request From peers
    def handle_peer_request(self, peer_socket):
        try:
            while True:
                bytes_received = peer_socket.recv(BUFFER_SIZE)

                if bytes_received:
                    if get_message_type(bytes_received) == "DOWNLOAD":
                        self.send_file_to_peer(bytes_received, peer_socket)
                else:
                    break

        except socket.error as e:
            print("Socket Error: " + str(e))

        peer_socket.close()

    # Use the bytes received and the know socket to send the file for download by the other client
    def send_file_to_peer(self, bytes_received, peer_socket):
        # use the bytes received to create an object of type Download
        download = Download(**bytes_to_object(bytes_received))
        # Assign file to be download to the download object
        file_name = download.file_name
        path_to_file = os.getcwd() + "/ClientFiles/" + file_name

        if not os.path.exists(path_to_file):
            download_error = DownloadError(download.rq, "File does not exist.")
            print(download_error)
            # TODO: send back download denied
            self.send_message_to_peer(download_error, peer_socket)
        # If File Exists, we can only send it by chunks of 200 characters therefore :
        else:
            with open(file=path_to_file, mode="r") as f:
                file_content = f.read()
                # The chunk starts empty
                chunk_text = ""
                chunk_number = 0
                # We loop through all the characters written within the file to be download by the peer
                for character in range(0, len(file_content)):
                    # If we arrive at the last chunk we enter this if statement,
                    # send the last chunk and break out of the loop
                    if character == len(file_content) - 1:
                        chunk_text += file_content[character]
                        # Chunk is full, create a object of type FileEnd to send the last piece of text from within the file
                        file_end = FileEnd(
                            download.rq, download.file_name, chunk_number, chunk_text)
                        self.send_message_to_peer(file_end, peer_socket)
                        log(file_end)
                        break
                    # For every other chunks, they are sent here,
                    # through the use of a file objects containing the chunk
                    elif character != 0 and (character + 1) % 200 == 0:
                        file = File(download.rq, download.file_name,
                                    chunk_number, chunk_text)
                        # Here we send message to the peer containing the file with the 200 chars
                        self.send_message_to_peer(file, peer_socket)
                        # Reset the chunk for next package of characters
                        chunk_text = ""
                        chunk_number += 1
                        log(file)
                    # Add next character to the chunk
                    chunk_text += file_content[character]

    # Function used to send a message to the server.
    # First the object to be sent is transformed into bytes
    def send_message_to_server(self, message):
        bytes_to_send = object_to_bytes(message)
        # Using the Udp Socket the bytes are sent to the proper address
        # Upon arrival they will be transformed into an object again
        self.udp_socket.sendto(bytes_to_send, self.server_address)
        # Increment the Rq as each message sent to server or client will be a new request number
        self.increment_rq()
        log(message)

    # Similarly here, we want to send a message to the peer
    # Transform Object to Byte and send it
    def send_message_to_peer(self, message, peer_socket):
        bytes_to_send = object_to_bytes(message)
        # Sending the bytes to the TCP address of the other client/peer
        peer_socket.send(bytes_to_send)
        # Again increment as each request is unique
        self.increment_rq()
        log(message)

# Simple function to retrieve the available files in the folder ClientFiles
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
