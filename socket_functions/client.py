from .common import *


# initiate server connection
def connect_server(connected_socket, client_ID):

    try:
        # Send client ID to server
        send_message(connected_socket, (f"CONNECT {client_ID}"))
        response = receive_message(connected_socket)
        if response != "CONNECT: OK":
            print(
                f"Error: Expected 'CONNECT: OK' reponse from server but recieved: {response}")
            return None

    except:
        print(f"Error: Unknown error connecting to server")
        return None

    # Connection established
    return True
