import socket
import argparse
import socket_functions
from socket_functions.constants import *

if __name__ == "__main__":
    print(f"Client Started")

    # get port from args
    # TODO: add option to specify host
    parser = argparse.ArgumentParser("socketClient")
    parser.add_argument(
        "host", help=f"Host name for outgoing connections. Default: {HOST}", type=str, nargs="?", default=HOST)
    parser.add_argument(
        "port", help=f"Port number for outgoing connections. Default: {DEFAULT_PORT}", type=int, nargs="?", default=DEFAULT_PORT)
    args = parser.parse_args()

    # Connect to server
    hostIP = socket.gethostbyname(args.host)
    print(
        f"Attempting connection to: {args.host}:{args.port} -> {hostIP}:{args.port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        try:
            server_socket.connect((hostIP, args.port))
            socket_file = socket_functions.connect_server(
                server_socket)
        except:
            socket_file = None

        if socket_file == None:
            print(f"Connection failed. Exiting...")
            exit()
        else:
            # Server connected, start main loop
            print(f"Connection established")
            with server_socket:
                while True:

                    # Prompt user for command
                    print("""Select an option:
1. PUT
2. GET
3. DELETE
4. DISCONNECT""")
                    if DEBUG:
                        print("5. Manual Command")

                    selected_option = input("Input: ").strip()

                    # Send command to server, prompting user for any keys or data
                    if selected_option == "1":
                        data_to_send = f"PUT {input('PUT Key: ').strip()}\n{input('PUT Data: ').strip()}"
                    elif selected_option == "2":
                        data_to_send = f"GET {input('GET Key: ').strip()}"
                    elif selected_option == "3":
                        data_to_send = f"DELETE {input('DELETE Key: ').strip()}"
                    elif selected_option == "4":
                        data_to_send = "DISCONNECT"
                    elif selected_option == "5" and DEBUG:
                        data_to_send = input("Manual Command: ").strip()
                    else:
                        print(f"Invalid option")
                        continue

                    socket_functions.send_line(socket_file, f"{data_to_send}")

                    # get and parse response from the server
                    response = socket_functions.get_line(socket_file)
                    command, status = socket_functions.parse_response(
                        response)
                    if not response:
                        print(f"No response from server")
                        break
                    elif response == "DISCONNECT: OK":
                        print(f"Disconnected from server")
                        break
                    elif response == "PUT: ERROR" or response == "GET: ERROR" or response == "DELETE: ERROR":
                        print(f"Error completing command.")
                    elif response == "PUT: OK" or response == "DELETE: OK" or (command == "GET" and status):
                        if PRINT_VERBOSE_STATUS:
                            print(f"Command completed successfully.")
                    else:
                        print(
                            f"Unexpected response received. Quitting...")
                        break

    print(f"Exiting...")
