class ClientInfo(dict):
    def __init__(self, clientId = -1, description = ""):
        dict.__init__(self, clientId=clientId, description=description)
