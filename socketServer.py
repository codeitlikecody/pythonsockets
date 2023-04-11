import socket
import argparse

HOST = '127.0.0.1'
DEFAULT_PORT = 4242
RECIEVE_BUFFER_SIZE = 1024
PRINT_CLIENT_COMMANDS = True
PRINT_SERVER_COMMANDS = True
PRINT_VERBOSE_STATUS = True


# send message to connected client
def send_message(conn, message):
    if PRINT_SERVER_COMMANDS:
        print(f'Server: {message}')
    conn.sendall(message.encode())


# recieve message from connected client
def recieve_message(conn):
    data = conn.recv(RECIEVE_BUFFER_SIZE)
    if data:
        if PRINT_CLIENT_COMMANDS:
            print(f'Client: {data.decode()}')
        return data.decode()
    else:
        return None


# initiate client connection
def connect_client(connected_clients):
    try:
        command, client_ID = recieve_message(conn).split(" ", 1)
        if command == 'CONNECT' and connected_clients.count(client_ID) == 0:
            connected_clients.append(client_ID)
            response = 'CONNECT: OK'
            if PRINT_VERBOSE_STATUS:
                print(f'Connected client with ID: {client_ID}')
        else:
            response = 'CONNECT: ERROR'
            if PRINT_VERBOSE_STATUS:
                print(
                    f'Error: Already connected to client with ID: {client_ID}')
    except:
        response = 'CONNECT: ERROR'
        if PRINT_VERBOSE_STATUS:
            print(
                f'Error: Unknown error occured while connecting client')
    return response, client_ID


# remove client connection
def disconnect_client(connected_clients, client_ID):
    # TODO: check if we need to delete client ID if client disconnects unexpectedly
    try:
        connected_clients.remove(client_ID)
        if PRINT_VERBOSE_STATUS:
            print(f'Disconnected client with ID: {client_ID}')
    except:
        if PRINT_VERBOSE_STATUS:
            print(
                f'Error: Could not remove client connection record')


print(f'Server Started')

# get port from args
parser = argparse.ArgumentParser("socketServer")
parser.add_argument(
    "port", help="Port number for incoming connections", type=int, nargs='?', default=DEFAULT_PORT)
args = parser.parse_args()
connected_clients = []

print(f'Listening on: {HOST}:{args.port}')
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, args.port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f'Connection recieved from: {addr}')

            # check for valid user ID
            response, client_ID = connect_client(connected_clients)
            send_message(conn, response)

            if response != 'CONNECT: OK':
                print(f'Connection failed. Waiting for new connection...')
            else:
                # Connection established, start main loop
                while True:
                    data = conn.recv(RECIEVE_BUFFER_SIZE)
                    if not data:
                        break
                    # handle recieved data
                    if PRINT_CLIENT_COMMANDS:
                        print(f'Client: {data.decode()}')

                    response = data.strip().decode()
                    # send response back to client
                    send_message(conn, response)

                # Connection lost, remove client from connected clients list
                disconnect_client(connected_clients, client_ID)
                print(f'Connection lost. Waiting for new connection...')
