from .constants import *


# send message to connected server or client
def send_line(socket_file, message):
    try:
        socket_file.write((f"{message}\n"))
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
