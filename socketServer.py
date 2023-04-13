import socket
import argparse
import socket_functions
from socket_functions.constants import *


if __name__ == '__main__':
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
            s, addr = s.accept()
            with s:
                print(f'Connection recieved from: {addr}')

                # attempt connection to client
                client_ID = socket_functions.connect_client(
                    s, connected_clients)
                if client_ID == None:
                    print(f'Connection to client failed. Waiting for new connection...')
                else:
                    # Connection established, start main loop
                    if PRINT_VERBOSE_STATUS:
                        print(
                            f'Connection to client {client_ID} successful. Waiting for commands...')
                    while True:
                        response = socket_functions.receive_message(s)
                        if not response:
                            break
                        # handle recieved data

                        response = response.strip()
                        # send response back to client
                        socket_functions.send_message(s, response)

                    # Connection lost, remove client from connected clients list
                    socket_functions.disconnect_client(
                        connected_clients, client_ID)
                    print(f'Connection lost. Waiting for new connection...')
