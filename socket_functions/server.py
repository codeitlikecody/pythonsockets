from .common import *


# initiate client connection
def connect_client(server_socket, port, connected_clients):
    client_socket = None
    try:
        # attempt connection to client
        server_socket.bind((HOST, port))
        server_socket.listen()
        client_socket, addr = server_socket.accept()
        print(f"Connection initiated on port: {addr[1]}")
        socket_file = client_socket.makefile('rw')

        # Get client ID from client and check existing connections
        response = "CONNECT: ERROR"
        command, client_ID = get_line(socket_file).split(" ", 1)
        if command != "CONNECT":
            client_ID = None
            if PRINT_VERBOSE_STATUS:
                print(
                    f"Error: Expected CONNECT command but recieved: {command}")
        elif connected_clients.count(client_ID) != 0:
            client_ID = None
            if PRINT_VERBOSE_STATUS:
                print(
                    f"Error: Already connected to client with ID: {client_ID}")
        else:
            connected_clients.append(client_ID)
            response = "CONNECT: OK"
            if PRINT_VERBOSE_STATUS:
                print(f"Connecting client with ID: {client_ID}")

    except ValueError as ex:
        client_ID = None
        if PRINT_VERBOSE_STATUS:
            print(
                f"Error: Unable to parse client command: {ex.args}")

    except OSError as ex:
        client_ID = None
        if PRINT_VERBOSE_STATUS:
            print(
                f"Error: Unable to connect to client: {ex.args[1]}")
        exit()

    except Exception as ex:
        client_ID = None
        if PRINT_VERBOSE_STATUS:
            print(
                f"Error: An {type(ex).__name__} exception occured while connecting client: {ex.args}")

    # send response to client
    if client_socket:
        send_line(socket_file, response)
    return client_socket, socket_file, client_ID


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

# handle a PUT message from client


def put(key, value, database):
    # check for valid key and value
    if key == None or value == None:
        return "PUT: ERROR"

    # update database
    database[key] = value
    if PRINT_VERBOSE_STATUS:
        print(f"PUT '{key}': '{value}'")
    return "PUT: OK"


# handle a GET message from client
def get(key, database):
    try:
        # get value from database
        value = database[key]
        if PRINT_VERBOSE_STATUS:
            print(f"GET '{key}': '{value}'")
        return f"GET {value}"
    except:
        # key not found
        if PRINT_VERBOSE_STATUS:
            print(f"Error: could not GET '{key}', key not found")
        return "GET: ERROR"


# handle a DELETE message from client
def delete(key, database):
    try:
        # delete value from database
        database.pop(key)
        if PRINT_VERBOSE_STATUS:
            print(f"DELETE '{key}'")
        return "DELETE: OK"
    except:
        # key not found
        if PRINT_VERBOSE_STATUS:
            print(f"Error: could not DELETE '{key}', key not found")
        return "DELETE: ERROR"
