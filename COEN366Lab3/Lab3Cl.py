import socket
import json
from json import JSONEncoder
import ClientInfo

    
# class JsonHelper(JSONEncoder):
#     def default(self, o):
#             return o.__dict__

msg = "hello"
SERVER = "127.0.0.1"
PORT = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
client_id = 0
client_info = ClientInfo.ClientInfo()

# send hello to the server
client.sendall(bytes(json.dumps(msg), "UTF-8"))

# wait for response
data = client.recv(1024)
resp = json.loads(data)
print("Client Info ser", data)

# check if receive message is Info
if isinstance(resp, dict):
    client_id = input("Enter Client Id")
    description = "NewClient " + client_id
    description = input("Enter Description")
    client_info = ClientInfo.ClientInfo(client_id, description)


# 
clientInfoJson = json.dumps(client_info)
print(clientInfoJson)
client.sendall(bytes(clientInfoJson, "UTF-8"))

client.close()
print("Client exit")
