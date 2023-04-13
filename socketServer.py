import socket
import argparse
import socket_functions
from socket_functions.constants import *


if __name__ == "__main__":
    print(f"Server Started")

    # get port from args
    parser = argparse.ArgumentParser("socketServer")
    parser.add_argument(
        "port", help="Port number for incoming connections", type=int, nargs="?", default=DEFAULT_PORT)
    args = parser.parse_args()
    connected_clients = []

    # define and close socket to reset it if server didn't close properly last time
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.close()

    print(f"Listening on: {HOST}:{args.port}")
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # attempt connection to client
            client_socket, client_ID = socket_functions.connect_client(
                server_socket, args.port, connected_clients)
            if client_socket == None:
                print(f"Connection to client failed. Waiting for new connection...")
            else:
                with client_socket:
                    # Connection established, start main loop
                    if PRINT_VERBOSE_STATUS:
                        print(
                            f"Connection to client {client_ID} successful. Waiting for commands...")
                    while True:
                        response = socket_functions.receive_message(
                            client_socket)
                        if not response:
                            break
                        # handle recieved data

                        response = response.strip()
                        # send response back to client
                        socket_functions.send_message(client_socket, response)

                    # Connection lost, remove client from connected clients list
                    socket_functions.disconnect_client(
                        connected_clients, client_ID)
                    print(f"Connection lost. Waiting for new connection...")
