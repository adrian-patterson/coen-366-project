import socket
import json
import ClientInfo


sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)      # For UDP

udp_host = "127.0.0.1"		        # Host IP
udp_port = 8080			                # specified port to connect

#print type(sock) ============> 'type' can be used to see type 
				# of any variable ('sock' here)

sock.bind((udp_host,udp_port))

while True:
	print ("Waiting for client...")
	data,addr = sock.recvfrom(1024)	        #receive data from client
	print ("Received Messages:",data," from",addr)