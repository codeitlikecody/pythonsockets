import rsa
import getpass
import hashlib
from .common import *


# initiate server connection
def connect_server(connected_socket):

    try:
        # Send client ID to server
        client_ID = input("Please enter client ID: ").strip()
        client_pass = getpass.getpass("Please enter password: ")
        salt = b'\xed\x12\x92\xc6\x86\xb4\x8a\xbf\x10\xb3bd\x1c/m\xca'
        hashed_pw = hashlib.pbkdf2_hmac(
            'sha256', client_pass.encode(), salt, 100000)

        # Create socket file and connect to server
        # socket_file = connected_socket.makefile('rw')
        # connected_socket.send(f"CONNECT {client_ID}\n")
        send_line(connected_socket, (f"CONNECT {client_ID}"))
        connected_socket.send(hashed_pw)
        response = get_line(connected_socket)
        if response != "CONNECT: OK":
            print(
                f"Error: Expected 'CONNECT: OK' response from server but received: {response}")
            return None

    except Exception as ex:
        print(
            f"Error: An {type(ex).__name__} exception occurred while connecting to server: {ex.args}")
        return None

    # Connection established
    return response
