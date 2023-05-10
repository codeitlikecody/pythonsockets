import socket
import argparse
import socket_functions
import rsa
import ssl

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
            sslSettings = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            sslSettings.load_cert_chain(
                "./certs/server-certificate.pem", keyfile="./certs/server-key.pem")
            secure_server_socket = ssl.SSLContext.wrap_socket(
                sslSettings, server_socket, server_side=True)
            secure_server_socket.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # attempt connection to client
            client_socket, client_ID = socket_functions.connect_client(
                secure_server_socket, args.port, connected_clients)
            if client_ID == None:
                print(f"Connection to client failed. Waiting for new connection...")
            else:
                with client_socket:
                    # Connection established
                    connected = True
                    if PRINT_VERBOSE_STATUS:
                        print(
                            f"Connection to client {client_ID} successful.")

                    # Secure connection established, start main loop
                    if PRINT_VERBOSE_STATUS:
                        print(
                            f"Connection secured. Waiting for commands...")
                    while connected:
                        response = socket_functions.get_line(
                            client_socket)
                        if not response:
                            break
                        # handle received data
                        command, key = socket_functions.parse_response(
                            response)
                        if command == "PUT" and key:
                            key, value = key.split("\n")
                            response = socket_functions.put(
                                key, value, database)
                        elif command == "GET" and key:
                            response = socket_functions.get(
                                key, database)
                        elif command == "DELETE" and key:
                            response = socket_functions.delete(
                                key, database)
                        elif command == "DISCONNECT":
                            response = "DISCONNECT: OK"
                            connected = False
                        else:
                            connected = False
                            if PRINT_VERBOSE_STATUS:
                                print(
                                    f"Error: Unknown or incorrectly formed command received: {command}")
                            break

                        # send response back to client
                        socket_functions.send_line(
                            client_socket, response)

                    # Connection lost, remove client from connected clients list
                    socket_functions.disconnect_client(
                        connected_clients, client_ID)

                    # try to gracefully close connection with client
                    client_socket.shutdown(socket.SHUT_RDWR)
                    client_socket.close()
                    print(f"Connection lost. Waiting for new connection...")
