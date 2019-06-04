# Standard Library imports
import socket
import time
import sys

# Custom Library imports
import api

# Constants
REQUEST_SIZE = 1024 # 1kb maximum request size. 
WAITING_CONNECTIONS = 5 # Number of waiting connections to be handled

class Server():
    def __init__(self, host, port):
        self.host = str(host)
        self.port = int(port)
        self.mainLoop()
    def mainLoop(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(WAITING_CONNECTIONS)
            while True:
                conn, addr = s.accept()
                with conn:
                    print("Connected by", addr)
                    data = conn.recv(REQUEST_SIZE)
                    if not data:
                        ret_data = "ERROR EMPTY REQUEST"
                    else:
                        api_call = data.decode('utf-8')
                        api_call = api_call.split(" ")[1]
                        ret_data = api.call(api_call)
                    conn.sendall(api.buildResponse(ret_data).encode())
