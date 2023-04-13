import socket
import argparse
import socket_functions
from socket_functions.constants import *

if __name__ == "__main__":
    print(f"Client Started")
    client_ID = input("Please enter client ID: ").strip()

    # get port from args
    parser = argparse.ArgumentParser("socketClient")
    parser.add_argument(
        "port", help="Port number for outgoing connections", type=int, nargs="?", default=DEFAULT_PORT)
    args = parser.parse_args()

    print(f"Attempting connection to: {HOST}:{args.port}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        try:
            server_socket.connect((HOST, args.port))
        except:
            print(f"Connection to {HOST}:{args.port} failed. Exiting...")
            exit()

        if socket_functions.connect_server(server_socket, client_ID) == None:
            print(f"Connection failed. Exiting...")
            exit()

        while True:
            print("""
1. PUT
2. GET
3. DELETE
4. DISCONNECT
5. Manual entry (debugging only)""")
            data_to_send = input("Input:").strip()

            server_socket.sendall((f"{data_to_send}").encode())
            response = server_socket.recv(RECEIVE_BUFFER_SIZE)
            if not response:
                break
            print(f"Received: {response.decode()}")

        print(f"Connection lost")

    print(f"Exiting...")
