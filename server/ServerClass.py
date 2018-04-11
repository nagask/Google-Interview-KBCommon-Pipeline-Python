import json
import socket
import datetime

import SocketServer

from .ServerTCPHandler import ServerTCPHandler

class ServerClass(object):

    def __init__(self):

        self.TCP_IP = None
        self.TCP_PORT = None
        self.BUFFER_SIZE = None
        self.LOG_DIR = None


    def config(self, server_config):

        self.TCP_IP = server_config.get("TCP_IP")
        self.TCP_PORT = server_config.get("TCP_PORT")
        self.BUFFER_SIZE = server_config.get("BUFFER_SIZE")
        self.LOG_DIR = server_config.get("LOG_DIR")

    def start(self):

        server = SocketServer.TCPServer((self.TCP_IP, self.TCP_PORT), ServerTCPHandler)
        server.serve_forever()
