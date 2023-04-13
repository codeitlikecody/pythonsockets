import socket
import argparse
import socket_functions
from socket_functions.constants import *

if __name__ == '__main__':
    print(f'Client Started')
    client_ID = input("Please enter client ID: ").strip()

    # get port from args
    parser = argparse.ArgumentParser("socketClient")
    parser.add_argument(
        "port", help="Port number for outgoing connections", type=int, nargs='?', default=DEFAULT_PORT)
    args = parser.parse_args()

    print(f'Attempting connection to: {HOST}:{args.port}')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, args.port))
        except:
            print(f'Connection to {HOST}:{args.port} failed. Exiting...')
            exit()

        s.sendall((f'CONNECT {client_ID}').encode())
        data = s.recv(RECEIVE_BUFFER_SIZE)
        if data:
            print(f'Received: {data.decode()}')

            command = data.decode()
            if command != 'CONNECT: OK':
                print(f'Connection failed. Exiting...')
                exit()

            while True:
                print("""
    1. PUT
    2. GET
    3. DELETE
    4. DISCONNECT
    5. Manual entry (debugging only)""")
                data_to_send = input("Input:").strip()

                s.sendall((f'{data_to_send}').encode())
                data = s.recv(RECEIVE_BUFFER_SIZE)
                if not data:
                    break
                print(f'Received: {data.decode()}')

        print(f'Connection lost')

    print(f'Exiting...')
