import rsa
import getpass
import hashlib
from .common import *


# initiate server connection
def connect_server(connected_socket, publicKey, privateKey):

    try:
        # Send client ID to server
        client_ID = input("Please enter client ID: ").strip()
        client_pass = getpass.getpass("Please enter password: ")
        salt = b'\xed\x12\x92\xc6\x86\xb4\x8a\xbf\x10\xb3bd\x1c/m\xca'
        hashed_pw = hashlib.pbkdf2_hmac('sha256', client_pass.encode(), salt, 100000)

        # Exchange public keys with server
        connected_socket.send(publicKey.save_pkcs1("PEM"))
        serverPublicKey = rsa.PublicKey.load_pkcs1(connected_socket.recv(RECEIVE_BUFFER_SIZE))
        # Create socket file and connect to server
        # socket_file = connected_socket.makefile('rw')
        send_line(connected_socket, (f"CONNECT {client_ID}"), serverPublicKey)
        connected_socket.send(hashed_pw)
        response = get_line(connected_socket, privateKey)
        if response != "CONNECT: OK":
            print(
                f"Error: Expected 'CONNECT: OK' response from server but received: {response}")
            return None

    except Exception as ex:
        print(f"Error: An {type(ex).__name__} exception occurred while connecting to server: {ex.args}")
        return None

    # Connection established
    return serverPublicKey
