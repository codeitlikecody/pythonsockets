import rsa
import zlib
from .constants import *


# send message to connected server or client
def send_line(connected_socket, message):
    try:

        # send CRC
        # crc = f"{zlib.crc32(message.encode())}"
        # encCrc = rsa.encrypt(crc.encode(),
        #                      publicKey)
        # connected_socket.send(encCrc)

        # send message
        # encMessage = rsa.encrypt(message.encode(),
        #                          publicKey)
        connected_socket.send(message.encode())

        if PRINT_SENT_COMMANDS:
            print(f"Sent: {message.strip()}")

        # wait for CRC response
        # crcResponse = connected_socket.recv(RECEIVE_BUFFER_SIZE)
        # if crcResponse == zlib.crc32(message):
        #     if PRINT_VERBOSE_STATUS:
        #         print(f"CRC: OK")
        # else:
        #     print(f"CRC: ERROR")
        #     return None

    except Exception as ex:
        if PRINT_VERBOSE_STATUS:
            print(
                f"Error: An {type(ex).__name__} exception occurred while sending line: {ex.args}")
        return None


# receive message from connected server or client
def get_line(connected_socket):
    try:
        message = connected_socket.recv(RECEIVE_BUFFER_SIZE).decode()
        if message:

            if PRINT_RECEIVED_COMMANDS:
                print(f"Received: {message}")

            # send CRC
            # crc = zlib.crc32(message.encode()).to_bytes(4, byteorder='big')
            # connected_socket.send(crc)
            return message
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
