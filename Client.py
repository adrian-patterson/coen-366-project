#This file contains calsses related to clients

# Contact information for the clients
class ContactInfo:
    def __init__(self, name = "", ip = "", udp = -1, tcp = -1 ):
        self.name = name
        self.ip = ip
        self.udp = udp
        self.tcp = tcp
