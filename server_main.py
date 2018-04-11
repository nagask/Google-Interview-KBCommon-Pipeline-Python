import sys
import os
import json

from server.ServerClass import ServerClass


if __name__ == "__main__":
    args = sys.argv

    server_config = json.load(open("config/server_config.json", 'r')).get("server")

    print("Server is running.")
    server = ServerClass()
    server.config(server_config)
    server.start()
