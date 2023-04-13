from .common import *


# initiate client connection
def connect_client(conn, connected_clients):
    try:
        # Get client ID from client and check existing connections
        command, client_ID = receive_message(conn).split(" ", 1)
        if command != 'CONNECT':
            response = 'CONNECT: ERROR'
            client_ID = None
            if PRINT_VERBOSE_STATUS:
                print(
                    f'Error: Expected CONNECT command but recieved: {command}')
        else:
            if connected_clients.count(client_ID) != 0:
                response = 'CONNECT: ERROR'
                client_ID = None
                if PRINT_VERBOSE_STATUS:
                    print(
                        f'Error: Already connected to client with ID: {client_ID}')
            else:
                connected_clients.append(client_ID)
                response = 'CONNECT: OK'
                if PRINT_VERBOSE_STATUS:
                    print(f'Connecting client with ID: {client_ID}')

    except:
        response = 'CONNECT: ERROR'
        client_ID = None
        if PRINT_VERBOSE_STATUS:
            print(
                f'Error: Unknown error occured while connecting client')

    # send response to client
    send_message(conn, response)
    return client_ID


# remove client connection
def disconnect_client(connected_clients, client_ID):
    # TODO: check if we need to delete client ID if client disconnects unexpectedly
    try:
        connected_clients.remove(client_ID)
        if PRINT_VERBOSE_STATUS:
            print(f'Disconnected client with ID: {client_ID}')
    except:
        if PRINT_VERBOSE_STATUS:
            print(
                f'Error: Could not remove client connection record')
