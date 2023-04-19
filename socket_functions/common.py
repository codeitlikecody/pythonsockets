from .constants import *


# send message to connected server or client
def send_line(socket_file, message):
    try:
        socket_file.write((f"{message}\n"))
        # flush buffer and send data now
        socket_file.flush()
        if PRINT_SENT_COMMANDS:
            print(f"Sent: {message.strip()}")
    except Exception as ex:
        if PRINT_VERBOSE_STATUS:
            print(
                f"Error: An {type(ex).__name__} exception occured while sending line: {ex.args}")
        return None


# receive message from connected server or client
def get_line(socket_file):
    try:
        data = socket_file.readline().strip()
        if data:
            if PRINT_RECEIVED_COMMANDS:
                print(f"Received: {data}")
            return data
        else:
            return None
    except Exception as ex:
        if PRINT_VERBOSE_STATUS:
            print(
                f"Error: An {type(ex).__name__} exception occured while reading line: {ex.args}")
        return None


# receive a command/key pair from the connected client
def parse_response(response):
    try:
        command, key = response.split(" ", 1)
        if PRINT_VERBOSE_STATUS:
            print(
                f"Command: {command} Key: {key}")
        return command.strip(), key.strip()

    # A command was recieved but no key, just return the key as None
    except ValueError as ex:
        if PRINT_VERBOSE_STATUS:
            print(
                f"Command: {response}")
        return response.strip(), None

    # Report and handle other parsing errors
    except Exception as ex:
        if PRINT_VERBOSE_STATUS:
            print(
                f"Error: An {type(ex).__name__} exception occured while parsing line: {ex.args}")
        return response.strip(), None
