from ssl import SSLSocket
from typing import Tuple
from .common import *

# for testing purposes, the following extremely secure client ID and passwords are active:
# admin -> 7(a6fm^YnfPC<$5Y
# abc -> 123

users = {("admin", b'uQ\xab\xf6Q\x19\xbd(\xe5\xa8\xc2\xca\x7f\xaey\xd1\xa9\x87\x97\x15\xf9i\x17\x05W>\xe9\xb8wZ\x8b\x11'),
         ("abc", b'g\xf8F4\xe6G]\x90\xc4\xa9\x8c%\xe2\xe7\x1ay<\x87\xdc=K*\xf5n\xdf\xfcG:u@:\xea')}

def connect_client(server_socket: SSLSocket, port: str, connected_clients: list) -> Tuple[SSLSocket, str]:
    """Initiate client connection
    
    Connects to a client and returns the client socket and ID if successful

    Parameters
    ----------
    server_socket : SSLSocket
        The server socket to use for the connection
    
    port : str
        The port to use for the connection

    connected_clients : list
        List of connected clients

    Returns
    -------
    Tuple[SSLSocket, str]
        The client socket and ID if successful, otherwise None
    """
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

    # handle errors
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


def disconnect_client(connected_clients: list, client_ID: str)  -> None:
    """Remove client connection

    Removes this client from the list of connected clients
    
    Parameters
    ----------
    connected_clients : list
        List of connected clients

    client_ID : str
        Ihe ID of the client to disconnect

    Returns
    -------
    None
    """
    # TODO: check if we need to delete client ID if client disconnects unexpectedly
    try:
        connected_clients.remove(client_ID)
        if PRINT_VERBOSE_STATUS:
            print(f"Removed connection for client with ID: {client_ID}")
    except:
        if PRINT_VERBOSE_STATUS:
            print(
                f"Error: Could not remove client connection record")


def put(key: str, value: str, database: dict) -> str:
    """Handle a PUT message from client

    Put a key/value pair into the database and handle any errors. Returns a fully formed PUT response  ready to send to the client.

    Parameters
    ----------
    key : str
        The key to store in the database
    value : str
        The value to store in the database
    database : dict
        The database to store the key/value pair in

    Returns
    -------
    str
        A fully formed PUT response to send to the client. Contains the OK/ERROR result of the PUT operation
    """
    # check for valid key and value
    if key == None or value == None:
        return "PUT: ERROR"

    # update database
    database[key] = value
    if PRINT_VERBOSE_STATUS:
        print(f"PUT '{key}': '{value}'")
    return "PUT: OK"


def get(key: str, database: dict) -> str:
    """Handle a GET message from client
    
    Get a value from the database and handle any errors. Returns a fully formed GET response ready to send to the client.

    Parameters
    ----------
    key : str
        The key to search for in the database
    database : dict
        The database to get the key from

    Returns
    -------
    str
        A fully formed GET response to send to the client. Contains the value stored in teh given key and CRC or an error message if the key is not found

    """
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


def delete(key: str, database: dict) -> str:
    """Handle a DELETE message from client

    Delete the specified key from the database and handle any errors. Returns a fully formed DELETE response ready to send to the client.

    Parameters
    ----------
    key : str
        The key to delete from the database
    database : dict
        The database to delete the key from

    Returns
    -------
    str
        A fully formed GET response to send to the client. Contains the result of the DELETE operation
    """
    try:
        # delete value from database
        database.pop(key)
        if PRINT_VERBOSE_STATUS:
            print(f"DELETE '{key}'")
        return "DELETE: OK"
    except:
        # key not found - the key is not in the database.
        if PRINT_VERBOSE_STATUS:
            print(f"Could not DELETE '{key}', key not found.")
        # as the key doesn't exist, we can return OK
        return "DELETE: OK"
