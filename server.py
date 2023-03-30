
from Socket import Socket
import random
from typing import TypedDict, Any
from datetime import datetime
import json
from threading import Thread, active_count
from cryptography.fernet import Fernet


DISCONECTED_MESSAGE = 'DISCONECTED'
Format = 'utf-8'


class User_(TypedDict):
    id: int
    user_name: str
    temp_key: Any
    is_connected: bool
    password: str


class Client_(TypedDict):
    temp_key: Any
    connection: Any
    address: Any


# לכתוב טייפ להודעה
# לטעון קובץ הודעות בתחילת הפונקציה המרכזית למשתנה
# לעדכן את המשתנה בהודעה חדשה כל פעם שמגיע כזאת
# לשמור הודעות לדאטה בייס בכל ניתוק לקוח או שרת


Clients: list[Client_] = []
Users: list[User_] = []


Messages = []
Server = Socket(5001).socket


def castum_encrypt(message, key):
    fernet_suit = Fernet(str(key))
    return fernet_suit.encrypt(message)


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


def spredMessage(message):
    for Client in Clients:
        encrypted_message = castum_encrypt(message, Client['temp_key'])
        Client['connection'].send(str(encrypted_message).encode(Format))


def handle_disconect(connection, address, id):
    connection.close()
    for i in range(len(Clients)):
        if Clients[i]['address'] == address:
            del Clients[i]
    for user in Users:
        if user['id'] == id:
            user['is_connected'] = False
    # delete client from Clients List based on the address


def check_password_and_return_data(password):
    for user in Users:
        if user['password'] == password:
            user['is_connected'] = True
            user['temp_key'] = random.randint(1, 50)
            return user
    return False


def client_handler(connection, address):

    connection.send(
        str({'msg': "hi,this is a key"}).encode(Format))
    User_data = {}
    conected = True
    loged = False
    while conected:
        print('listing for messages....')
        if loged == False:
            message = connection.recv(1024).decode(Format)
            user_data = check_password_and_return_data(message)
            if user_data:
                User_data = user_data
                loged = True
                connection.send(str(user_data).encode(Format))
                Client = {
                    "user_id": user_data['temp_key'],
                    "connection": connection,
                    "address": address
                }
                Clients.append(Client)
        else:
            message = connection.recv(1024).decode(Format)

            spredMessage(message)
            save_message_to_db(message)
            print('message recivevd....',  message, ' from addres: ', address)
            if message == DISCONECTED_MESSAGE:
                print('client disconacted')
                conected = False
    handle_disconect(connection, address, User_data['id'])
    #  connection.close()


def get_users(file_name):
    with open(file_name, 'r') as my_file:
        data = json.load(my_file)
        return data


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
