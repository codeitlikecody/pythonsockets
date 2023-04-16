from .common import *
import time


# initiate server connection
def connect_server(connected_socket, client_ID):

    try:
        # Send client ID to server

        socket_file = connected_socket.makefile('rw')
        send_line(socket_file, (f"CONNECT {client_ID}"))
        response = get_line(socket_file)
        if response != "CONNECT: OK":
            print(
                f"Error: Expected 'CONNECT: OK' reponse from server but recieved: {response}")
            return None

    except:
        print(f"Error: Unknown error connecting to server")
        return None

    # Connection established
    return socket_file
