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

    # initialize variables
    connected_clients = []
    database = {}

    # define and close socket to reset it if server didn't close properly last time
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.close()

    print(f"Listening on: {HOST}:{args.port}")
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # attempt connection to client
            client_socket, socket_file, client_ID = socket_functions.connect_client(
                server_socket, args.port, connected_clients)
            if client_ID == None:
                print(f"Connection to client failed. Waiting for new connection...")
            else:
                with client_socket:
                    # Connection established, start main loop
                    connected = True
                    if PRINT_VERBOSE_STATUS:
                        print(
                            f"Connection to client {client_ID} successful. Waiting for commands...")
                    while connected:
                        response = socket_functions.get_line(
                            socket_file)
                        if not response:
                            break
                        # handle recieved data
                        command, key = socket_functions.parse_response(
                            response)
                        if command == "PUT":
                            value = socket_functions.get_line(socket_file)
                            response = socket_functions.put(
                                key, value, database)
                        elif command == "GET":
                            response = socket_functions.get(
                                key, database)
                        elif command == "DELETE":
                            response = socket_functions.delete(
                                key, database)
                        elif command == "DISCONNECT":
                            # TODO: handle DISCONNECT command
                            response = "DISCONNECT: OK"
                            connected = False
                        else:
                            connected = False
                            if PRINT_VERBOSE_STATUS:
                                print(
                                    f"Error: Unknown command recieved: {command}")
                            break

                        # send response back to client
                        socket_functions.send_line(socket_file, response)

                    # Connection lost, remove client from connected clients list
                    socket_functions.disconnect_client(
                        connected_clients, client_ID)
                    # TODO: try to gracefully close connection with client
                    client_socket.shutdown(socket.SHUT_RDWR)
                    client_socket.close()
                    print(f"Connection lost. Waiting for new connection...")
