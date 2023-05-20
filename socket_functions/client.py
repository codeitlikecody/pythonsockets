import getpass
import hashlib
from ssl import SSLSocket
from .common import *


def connect_server(connected_socket: SSLSocket) -> str|None:
    """Initiate server connection

    Connects to a server and returns the server response if successful

    Parameters
    ----------
    connected_socket : SSLSocket
        The socket to use for the connection

    Returns
    -------
    str
        The server response if successful, otherwise None
    """

    response = None

    try:
        # Send client ID to server
        client_ID = input("Please enter client ID: ").strip()
        client_pass = getpass.getpass("Please enter password: ")
        salt = b'\xed\x12\x92\xc6\x86\xb4\x8a\xbf\x10\xb3bd\x1c/m\xca'
        hashed_pw = hashlib.pbkdf2_hmac(
            'sha256', client_pass.encode(), salt, 100000)

        send_line(connected_socket, (f"CONNECT {client_ID}"))
        connected_socket.send(hashed_pw)
        response = get_line(connected_socket)
        if response != "CONNECT: OK":
            print(
                f"Error: Expected 'CONNECT: OK' response from server but received: {response}")
            return None

    # Connection failed - handle exceptions
    except Exception as ex:
        print(
            f"Error: An {type(ex).__name__} exception occurred while connecting to server: {ex.args}")
        return None

    # Connection established
    return response
