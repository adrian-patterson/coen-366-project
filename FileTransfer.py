### This file contains classes related to file transfering

#Once a client knows what file to download and how to reach the peer, it will first set a TCP
#connection to the peer, and then send the following message to download the file.
class Download:
    def __init__(self, rqNum = -1, fileName = ""):
        self.rqNum = rqNum
        self.fileName = fileName
    

#If the file exists at destination, the peer will start transferring the file in small chunks not
#exceeding 200 characters using the following message (where Chunk# indicates the
#order/place of the Text in the original file).
class File:
    def __init__(self, rqNum = -1, fileName = "", chunkNum = -1, text = ""):
        self.rqNum = rqNum
        self.fileName = fileName
        self.chunkNum = chunkNum
        self.text = text


#The last chunk of the file is carried in a special message to indicate the last portion of the file.
class FileEnd:
    def __init__(self, rqNum = -1, fileName = "", chunkNum = -1, text = ""):
        self.rqNum = rqNum
        self.fileName = fileName
        self.chunkNum = chunkNum
        self.text = text

#While receiving these messages the client who requested the file puts the chunks together to
#compose again the original file. Upon complete reception of the file the client closes the TCP
#connection.
#If the requested file does not exist at destination or for some other reasons the contacted peer
#cannot engage in a file transfer it sends the following message.

class DownloadError:
    def __init__(self, rqNum = -1, reason = ""):
        self.rqNum = rqNum
        self.reason = reason
    


