### This file contains classes related to retrieving information from the server
#  python json example https://www.w3schools.com/python/python_json.asp

import Client

# A registered user can retrieve information from the server by sending different kinds of
# requests. A user can retrieve for instance the names of all the other registered clients, how to
# reach them using TCP and the available files by sending the following message to the server. 
class  RetriveAll:
    def __init__(self, rqNum = -1):
        self.rqNum = rqNum

# For a registered user the server will responds with the names, IP addresses, TCP socket# and
# available files of all registered clients.
class Retrieve:
    def __init__(self, rqNum = -1, clientList = [{}]):
        self.rqNum = rqNum
        self.clientList = clientList #list of client's dicts

# For a non-registered user the server ignores the request.
# A registered user can also request the information about a specific peer. For this it needs to
# know the name and send the following request to server.
class RetrieveInfoReq:
    def __init__(self, rqNum = -1, clientName = ""):
        self.rqNum = rqNum
        self.clientName = clientName

# For a registered user the server will responds with the name, IP addresses and TCP socket# of
# the client named “Name” if it exists and is registered.
class RetrieveInfoRes:
    def __init__(self, rqNum = -1, clientInfo = {}):
        self.rqNum = rqNum
        self.clientInfo = clientInfo

# For a non-registered user the server ignores the request. However, if the requested name does
# not exists/not registered, the server will respond with
class RetrieveError:
    def __init__(self, rqNum = -1, reason = ""):
        self.rqNum = rqNum
        self.reason = reason

# The Reason could be “client does not exist/is not registered.
# A user can search for a specific file by sending the following message to the server.
class SerchFileReq:
    def __init__(self, rqNum = -1, fileName = ""):
        self.rqNum = rqNum
        self.fileName = fileName 

# If the file exists, the server responds with the names of all the registered clients from where
# this file can be downloaded with all the necessary information.
class SerchFileRes:
    def __init__(self, rqNum = -1, clientList = []):
        self.rqNum = rqNum
        self.clientList = clientList #list of client's info

# If the user is not registered, the search request is ignored. However, if the user is registered
# but the file does not exist, the server will respond with.
class SerchError:
    def __init__(self, rqNum = -1, reason = ""):
        self.rqNum = rqNum
        self.reason = reason 

