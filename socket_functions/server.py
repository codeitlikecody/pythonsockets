from .common import *


# initiate client connection
def connect_client(server_socket, port, connected_clients):
    try:
        # attempt connection to client
        server_socket.bind((HOST, port))
        server_socket.listen()
        client_socket, addr = server_socket.accept()
        print(f"Connection recieved from: {addr}")

        # Get client ID from client and check existing connections
        command, client_ID = receive_message(client_socket).split(" ", 1)
        if command != "CONNECT":
            response = "CONNECT: ERROR"
            client_ID = None
            if PRINT_VERBOSE_STATUS:
                print(
                    f"Error: Expected CONNECT command but recieved: {command}")
        else:
            if connected_clients.count(client_ID) != 0:
                response = "CONNECT: ERROR"
                client_ID = None
                if PRINT_VERBOSE_STATUS:
                    print(
                        f"Error: Already connected to client with ID: {client_ID}")
            else:
                connected_clients.append(client_ID)
                response = "CONNECT: OK"
                if PRINT_VERBOSE_STATUS:
                    print(f"Connecting client with ID: {client_ID}")

    except:
        response = "CONNECT: ERROR"
        client_ID = None
        if PRINT_VERBOSE_STATUS:
            print(
                f"Error: Unknown error occured while connecting client")

    # send response to client
    send_message(client_socket, response)
    return client_socket, client_ID


# remove client connection
def disconnect_client(connected_clients, client_ID):
    # TODO: check if we need to delete client ID if client disconnects unexpectedly
    try:
        connected_clients.remove(client_ID)
        if PRINT_VERBOSE_STATUS:
            print(f"Removed connection for client with ID: {client_ID}")
    except:
        if PRINT_VERBOSE_STATUS:
            print(
                f"Error: Could not remove client connection record")
