
from Socket import Socket
import random
from typing import TypedDict, Any
from datetime import datetime
import json
from threading import Thread, active_count
DISCONECTED_MESSAGE = 'DISCONECTED'
Format = 'utf-8'
users = [{
    'user_id': 892437598274,
    'user_name': 'moshe',
    'other_stuff': 'sasdasdasd'
}]


Server = Socket(5001).socket


def save_message_to_db(message, address):
    with open("messages.json", 'w') as my_zibi:
        data: list = json.load(my_zibi)
        now = datetime.now()

        new_message = {
            'time_stemp': now,
            'user_id': '098209348509',
            'address': address,
            'msg': message

        }
        data.append(new_message)
        json.dump(data, my_zibi)
    # להוסיף הודעה לקובץ הגייסון messages


class User_(TypedDict):
    "id": int
    "user_name": str
    "temp_key": Any
    "is_connected": bool
    "password": str


class Client_(TypedDict):

    connection: Any
    address: Any


Clients: list[Client_] = []
Users: list[User_] = []
# Clients = []


def spredMessage(message):
    for Client in Clients:
        Client['connection'].send(message.encode(Format))


def handle_disconect(connection, address):
    connection.close()
    for i in range(len(Clients)):
        if Clients[i]['address'] == address:
            del Clients[i]

    # delete client from Clients List based on the address


def client_handler(connection, address):
    Client = {

        "connection": connection,
        "address": address
    }
    Clients.append(Client)
    print(Clients)
    connection.send(
        str({'msg': "hi,this is a key"}).encode(Format))

    conected = True
    while conected:
        print('listing for messages....')
        message = connection.recv(1024).decode(Format)
        spredMessage(message)
        save_message_to_db(message)
        print('message recivevd....',  message, ' from addres: ', address)
        if message == DISCONECTED_MESSAGE:
            print('client disconacted')
            conected = False
    handle_disconect(connection, address)
    #  connection.close()


def get_users(file_name):
    with open(file_name, 'r') as my_file:
        return json.load(my_file)


def set_users(file_name, users_data):
    with open(file_name, 'w') as outfile:
        return json.dump(users_data, outfile)


def server_script():
    Users = get_users('users.json')
    Server.listen()

    while True:
        print('Waiting for CONNECTIONS...')
        connection, address = Server.accept()

        new_thred = Thread(
            target=client_handler, args=(connection, address))
        new_thred.start()
        print('total conected users: ', active_count()-1)


if __name__ == "__main__":
    server_script()


# ריבוי משתמשים C
# פונקציה כללית של כתיבה לDB
# מ app.py להריץ שרת ו3 יוזרים ששולחים הודעות שונות
