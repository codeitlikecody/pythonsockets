from .common import *


# initiate server connection
def connect_server(connected_socket):

    try:
        # Send client ID to server
        client_ID = input("Please enter client ID: ").strip()
        socket_file = connected_socket.makefile('rw')
        send_line(socket_file, (f"CONNECT {client_ID}"))
        response = get_line(socket_file)
        if response != "CONNECT: OK":
            print(
                f"Error: Expected 'CONNECT: OK' response from server but received: {response}")
            return None

    except:
        print(f"Error: Unknown error connecting to server")
        return None

    # Connection established
    return socket_file
