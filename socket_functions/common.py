from ssl import SSLSocket
import rsa
import zlib
from .constants import *


def send_line(connected_socket: SSLSocket, message: str) -> None:
    """Send a line of text to a connected socket
    
    Parameters
    ----------
    connected_socket : SSLSocket
        The socket to send the message to
    
    message : str
        The message to send

    Returns
    -------
    None
    """

    try:

        connected_socket.send(message.encode())

        if PRINT_SENT_COMMANDS:
            print(f"Sent: {message.strip()}")

    except Exception as ex:
        if PRINT_VERBOSE_STATUS:
            print(
                f"Error: An {type(ex).__name__} exception occurred while sending line: {ex.args}")
        return None


def get_line(connected_socket: SSLSocket) -> str|None:
    """Receive a line of text from a connected socket

    Parameters
    ----------
    connected_socket : SSLSocket
        The socket to receive the message from

    Returns
    -------
    str
        The received message if successful, otherwise None
    """

    try:
        message = connected_socket.recv(RECEIVE_BUFFER_SIZE).decode()
        if message:

            if PRINT_RECEIVED_COMMANDS:
                print(f"Received: {message}")

            return message
        else:
            return None
        
    # Connection closed by server - handle exceptions
    except Exception as ex:
        if PRINT_VERBOSE_STATUS:
            print(
                f"Error: An {type(ex).__name__} exception occurred while reading line: {ex.args}")
        return None


def parse_response(response: str) -> str|None:
    """Parse a response from a connected socket

    Parameters
    ----------
    response : str
        The response to parse

    Returns
    -------
    str
        The command if successful, otherwise None
    """

    try:
        command, key = response.split(" ", 1)
        if PRINT_VERBOSE_STATUS:
            print(
                f"Command: {command} Key: {key}")
        return command.strip(), key.strip()

    # A command was received but no key, just return the key as None
    except ValueError as ex:
        if PRINT_VERBOSE_STATUS:
            print(
                f"Command: {response}")
        return response.strip(), None

    # Report and handle other parsing errors
    except Exception as ex:
        if PRINT_VERBOSE_STATUS:
            print(
                f"Error: An {type(ex).__name__} exception occurred while parsing line: {ex.args}")
        return response.strip(), None
