import socket
import argparse

HOST = '127.0.0.1'
DEFAULT_PORT = 4242
RECIEVE_BUFFER_SIZE = 1024
PRINT_CLIENT_COMMANDS = True
PRINT_SERVER_COMMANDS = True

print(f'Server Started')

# get port from args
parser = argparse.ArgumentParser("socketServer")
parser.add_argument(
    "port", help="Port number for incoming connections", type=int, nargs='?', default=DEFAULT_PORT)
args = parser.parse_args()


print(f'Listening on: {HOST}:{args.port}')
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, args.port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f'Connection recieved from: {addr}')

            data = conn.recv(RECIEVE_BUFFER_SIZE)
            if not data:
                break

            # check for valid user ID
            if PRINT_CLIENT_COMMANDS:
                print(f'Client: {data.decode()}')

            command, data = data.decode().split(" ", 1)
            if command == 'CONNECT':
                response = 'CONNECT: OK'
            else:
                response = 'CONNECT: ERROR'

            # send response back to client
            if PRINT_CLIENT_COMMANDS:
                print(f'Server: {response}')

            conn.sendall(response.encode())

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
                if PRINT_CLIENT_COMMANDS:
                    print(f'Server: {response}')

                conn.sendall(response.encode())

            print(f'Connection lost. Waiting for new connection...')
