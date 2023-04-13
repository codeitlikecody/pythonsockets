from .common import *


# initiate server connection
def connect_server(s, client_ID):

    try:
        # Send client ID to server
        send_message(s, (f'CONNECT {client_ID}'))
        response = receive_message(s)
        if response != 'CONNECT: OK':
            print(
                f'Error: Expected CONNECT: OK reponse from server but recieved: {response}')
            return None

    except:
        print(f'Error: Unknown error connecting to server')
        return None

    # Connection established
    return True
