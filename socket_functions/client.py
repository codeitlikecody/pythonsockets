import rsa
from .common import *


# initiate server connection
def connect_server(connected_socket, publicKey, privateKey):

    try:
        # Send client ID to server
        client_ID = input("Please enter client ID: ").strip()

        # Exchange public keys with server
        connected_socket.send(publicKey.save_pkcs1("PEM"))
        serverPublicKey = rsa.PublicKey.load_pkcs1(connected_socket.recv(RECEIVE_BUFFER_SIZE))

        # Create socket file and connect to server
        # socket_file = connected_socket.makefile('rw')
        send_line(connected_socket, (f"CONNECT {client_ID}"), serverPublicKey)
        response = get_line(connected_socket, privateKey)
        if response != "CONNECT: OK":
            print(
                f"Error: Expected 'CONNECT: OK' response from server but received: {response}")
            return None

    except:
        print(f"Error: Unknown error connecting to server")
        return None

    # Connection established
    return serverPublicKey
