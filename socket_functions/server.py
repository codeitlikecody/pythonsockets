import rsa
from .common import *

# for testing purposes, the following extremely secure client ID and passwords are active:
# admin -> 7(a6fm^YnfPC<$5Y
# abc -> 123


users = {("admin", b'uQ\xab\xf6Q\x19\xbd(\xe5\xa8\xc2\xca\x7f\xaey\xd1\xa9\x87\x97\x15\xf9i\x17\x05W>\xe9\xb8wZ\x8b\x11'),
         ("abc", b'g\xf8F4\xe6G]\x90\xc4\xa9\x8c%\xe2\xe7\x1ay<\x87\xdc=K*\xf5n\xdf\xfcG:u@:\xea')}

# initiate client connection


def connect_client(server_socket, port, connected_clients):
    client_socket = None
    try:
        # attempt connection to client
        server_socket.bind((HOST, port))
        server_socket.listen()
        client_socket, addr = server_socket.accept()
        print(f"Connection initiated on port: {addr[1]}")

        # Get client ID and hashed password
        response = "CONNECT: ERROR"
        command, client_ID = get_line(client_socket).split(" ", 1)
        client_password = client_socket.recv(PASS_HASH_SIZE)

        # Check for valid command
        if command != "CONNECT":

            client_ID = None
            if PRINT_VERBOSE_STATUS:
                print(
                    f"Error: Expected CONNECT command but received: {command}")

        # check for existing connection from this client
        elif connected_clients.count(client_ID) != 0:
            client_ID = None
            if PRINT_VERBOSE_STATUS:
                print(
                    f"Error: Already connected to client with ID: {client_ID}")
        else:
            # Check client password
            for client, password in users:
                if client == client_ID and password == client_password:
                    connected_clients.append(client_ID)
                    response = "CONNECT: OK"
                    if PRINT_VERBOSE_STATUS:
                        print(f"Connecting client with ID: {client_ID}")
                    break
            else:
                if PRINT_VERBOSE_STATUS:
                    print(
                        f"Error client with ID: {client_ID}. No matching user/password")

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
                f"Error: An {type(ex).__name__} exception occurred while connecting client: {ex.args}")

    # send response to client
    if client_socket:
        send_line(client_socket, response)
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
        # get value from database and calculate CRC
        value = database[key]
        crc = zlib.crc32(value.encode())
        if PRINT_VERBOSE_STATUS:
            print(f"GET '{key}': '{value}'")
        return f"GET {value}\n{crc}"
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
