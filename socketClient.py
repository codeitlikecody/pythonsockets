import socket
import argparse
import zlib
import socket_functions
import rsa
import ssl

from socket_functions.constants import *

if __name__ == "__main__":
    print(f"Client Started")

    # get port from args
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
            sslSettings = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            sslSettings.load_verify_locations("./certs/server-certificate.pem")
            sslSettings.check_hostname = False
            secure_server_socket = ssl.SSLContext.wrap_socket(
                sslSettings, server_socket, server_side=False, server_hostname=hostIP)

            secure_server_socket.connect((hostIP, args.port))

            # Attempt connection to server
            server_response = socket_functions.connect_server(
                secure_server_socket)
        except Exception as ex:
            print(
                f"Error: An {type(ex).__name__} exception occurred while connecting to server: {ex.args}")
            server_response = None

        if server_response == None:
            print(f"Connection failed. Exiting...")
            exit()
        else:

            # Server connected, start main loop
            print(f"Secure connection established")

            with secure_server_socket:
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

                    socket_functions.send_line(
                        secure_server_socket, f"{data_to_send}")

                    # get and parse response from the server
                    response = socket_functions.get_line(
                        secure_server_socket)
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
                    elif command == "GET" and status:
                        value, expected_crc = status.split("\n", 1)
                        calculated_crc = zlib.crc32(value.encode())
                        if calculated_crc == int(expected_crc):
                            if PRINT_VERBOSE_STATUS:
                                print(
                                    f"GET command completed successfully. Value: {value} CRC: {expected_crc}")
                        else:
                            if PRINT_VERBOSE_STATUS:
                                print(
                                    f"GET command failed. CRC check failed.")
                    elif response == "PUT: OK":
                        if PRINT_VERBOSE_STATUS:
                            print(f"PUT command completed successfully.")
                    elif response == "PUT: OK" or response == "DELETE: OK":
                        if PRINT_VERBOSE_STATUS:
                            print(f"DELETE command completed successfully.")
                    else:
                        print(
                            f"Unexpected response received. Quitting...")
                        break

    print(f"Exiting...")
