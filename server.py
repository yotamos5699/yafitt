
import threading
from Socket import Socket
import random
from typing import TypedDict, Any

DISCONECTED_MESSAGE = 'DISCONECTED'
Format = 'utf-8'


Server = Socket(5001).server


class Client_(TypedDict):
    key: int
    connection: Any
    address: Any


Clients: list[Client_] = []
# Clients = []


def spredMessage(message):
    for Client in Clients:
        Client['connection'].send(message).encode(Format)


def client_handler(connection, address):
    Client = {
        "key": random.randomint(1, 50),
        "connection": connection,
        "address": address
    }
    Clients.append(Client)
    Client['connection'].send("hi,this is a key", Client['key']).encode(Format)

    conected = True
    while conected:
        print('listing for messages....')
        message = connection.recv().decode(Format)
        spredMessage(message)
        print('message recivevd....',  message, ' from addres: ', address)
        if message == DISCONECTED_MESSAGE:
            print('client disconacted')
            conected = False
    connection.close()


def server_script():

    Server.listen()
    while True:
        print('Waiting for CONNECTIONS...')
        connection, address = Server.accept()
        threading.Thread(target=client_handler, arg=(connection, address))
        print('total conected users: ', threading.active_count()-1)


if __name__ == "__main__":
    server_script()
