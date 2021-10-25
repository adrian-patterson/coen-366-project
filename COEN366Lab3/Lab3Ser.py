#Example https://www.geeksforgeeks.org/tcp-and-udp-server-using-select/
#Example https://cppsecrets.com/users
# /110711510497115104971101075756514864103109971051084699111109/Python-UDP-Server-with-Multiple-Clients.php

import socket, threading
import json
import ClientInfo

client_list = []
response = ""
client_info_list = []
LOCALHOST = "127.0.0.1"
PORT = 8080


def updateClientInfo(msg):
    client_info_list.append(msg)
    print("Client Info List updated ", len(client_info_list))

# Thread per tcp client
class ClientThread(threading.Thread):
    def __init__(self, client_tcp_sock):
        threading.Thread.__init__(self)
        self.csocket = client_tcp_sock
    def run(self):
        msg = ''
        #serialize into the object
        data = self.csocket.recv(2048)
        msg = json.loads(data) 
        
        # check hello message from a client
        if isinstance(msg, str) and msg =='hello':
            print("RECEIVED HELLO")
            client_info = ClientInfo.ClientInfo()
            response = json.dumps(client_info)
            self.csocket.send(bytes(response, "UTF-8"))


        data = self.csocket.recv(2048)
        msg = json.loads(data) 
        print("Client Info res" , msg)

        # assume client is reliable no error
        if isinstance(msg, dict):
            #update client info list
            updateClientInfo(msg)

        #print(client_info_list[len(client_info_list) -1])
        
        # every 4 clients update archive list
        if len(client_info_list)%4 == 0:
            # store it to the archive server
            print("Talk to the archive server")
            client_info_listJson = json.dumps(client_info_list)
            self.client_udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            self.client_udp.sendto(bytes(client_info_listJson, "UTF-8"), (LOCALHOST,PORT))
            # data = self.client_udp.recvfrom(1024)
            # msg = json.loads(data)
            # print(msg)
            

server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_tcp.bind((LOCALHOST, PORT))
server_tcp.listen()
print("Server Strating")
print("Waiting for client request..")
while True:
    try:
        client_tcp_sock, addr = server_tcp.accept()
        new_client = ClientThread(client_tcp_sock)
        new_client.start()
        client_list.append(new_client)
        print("Accepted New Client")
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        raise SystemExit
    finally:
        print("Finally clause")
        for i in client_list:
            i.join()
            print("Exiting Threads...")


