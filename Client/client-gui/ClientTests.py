from Client import Client
from ClientRequests import *

MY_IP_ADDRESS = '10.0.0.12'

def RegisterClient():
    client = Client()
    client.name = "Test"
    register_with_server = RegisterWithServer(client, MY_IP_ADDRESS)
    register_with_server.start()
    register_with_server.join()

if __name__ == "__main__":

    RegisterClient()
