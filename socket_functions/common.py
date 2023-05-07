import rsa
from .constants import *


# send message to connected server or client
def send_line(connected_socket, message, publicKey):
    try:
        encMessage = rsa.encrypt(message.encode(),
                         publicKey)
        connected_socket.send(encMessage)
        # flush buffer and send data now
        # connected_socket.flush()
        if PRINT_SENT_COMMANDS:
            print(f"Sent: {message.strip()}")
    except Exception as ex:
        if PRINT_VERBOSE_STATUS:
            print(
                f"Error: An {type(ex).__name__} exception occurred while sending line: {ex.args}")
        return None


# receive message from connected server or client
def get_line(connected_socket, privateKey):
    try:
        data = connected_socket.recv(RECEIVE_BUFFER_SIZE)
        if data:
            decMessage = rsa.decrypt(data, privateKey).decode()
            if PRINT_RECEIVED_COMMANDS:
                print(f"Received: {decMessage}")
            return decMessage
        else:
            return None
    except Exception as ex:
        if PRINT_VERBOSE_STATUS:
            print(
                f"Error: An {type(ex).__name__} exception occurred while reading line: {ex.args}")
        return None


# receive a command/key pair from the connected client
def parse_response(response):
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
