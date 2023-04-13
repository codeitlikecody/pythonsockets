from .constants import *


# send message to connected server or client
def send_message(connected_socket, message):
    try:
        connected_socket.sendall(message.encode())
        if PRINT_SENT_COMMANDS:
            print(f"Sent: {message}")
    except:
        print(f"Error: Could not send message: {message}")
        return None


# receive message from connected server or client
def receive_message(connected_socket):
    try:
        data = connected_socket.recv(RECEIVE_BUFFER_SIZE)
        if data:
            if PRINT_RECEIVED_COMMANDS:
                print(f"Received: {data.decode()}")
            return data.decode()
        else:
            return None
    except:
        print(f"Error: Could not recieve message")
        return None
