
from Socket import Socket
import random
from typing import TypedDict, Any
from datetime import datetime
import json
from threading import Thread, active_count
from cryptography.fernet import Fernet

<<<<<<< HEAD
from typingClasses import Client_, Message_, User_

=======
>>>>>>> 84872b684fb5a8670f35b013e592646770a7c348

DISCONECTED_MESSAGE = 'DISCONECTED'
Format = 'utf-8'


<<<<<<< HEAD
=======
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


>>>>>>> 84872b684fb5a8670f35b013e592646770a7c348
# לכתוב טייפ להודעה
# לטעון קובץ הודעות בתחילת הפונקציה המרכזית למשתנה
# לעדכן את המשתנה בהודעה חדשה כל פעם שמגיע כזאת
# לשמור הודעות לדאטה בייס בכל ניתוק לקוח או שרת

<<<<<<< HEAD
def get_json1(file_name):
    with open(file_name, 'r') as my_file:
        data = json.load(my_file)
        return data


Clients: list[Client_] = []
Users: list[User_] = get_json1('db/users.json')
Messages: list[Message_] = get_json1('db/messages.json')

=======

Clients: list[Client_] = []
Users: list[User_] = []


Messages = []
>>>>>>> 84872b684fb5a8670f35b013e592646770a7c348
Server = Socket(5001).socket


def castum_encrypt(message, key):
    fernet_suit = Fernet(str(key))
    return fernet_suit.encrypt(message)
<<<<<<< HEAD
=======


def save_message_to_db(message, address):
    with open("messages.json", 'w') as my_zibi:
        data: list = json.load(my_zibi)
        now = datetime.now()
>>>>>>> 84872b684fb5a8670f35b013e592646770a7c348


def save_message_to_kash(message, user: User_):
    new_message: Message_ = {
        "time_stemp": datetime.now(),
        "owner_id": user['id'],
        "sender": user['user_name'],
        "message": message
    }
    Messages.append(new_message)
    return new_message

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
<<<<<<< HEAD
    set_json1('messages.json', Messages)
=======
>>>>>>> 84872b684fb5a8670f35b013e592646770a7c348
    # delete client from Clients List based on the address


def check_password_and_return_data(password):
<<<<<<< HEAD

    for user in Users:
        if user['password'] == password:

            user['is_connected'] = True
            user['temp_key'] = random.randint(1, 50)
            user['connections'] = user['connections'] + 1
            return user
    return False

=======
    for user in Users:
        if user['password'] == password:
            user['is_connected'] = True
            user['temp_key'] = random.randint(1, 50)
            return user
    return False

>>>>>>> 84872b684fb5a8670f35b013e592646770a7c348

def client_handler(connection, address):

    connection.send(
<<<<<<< HEAD
        str({'msg': "ok"}).encode(Format))
=======
        str({'msg': "hi,this is a key"}).encode(Format))
>>>>>>> 84872b684fb5a8670f35b013e592646770a7c348
    User_data = {}
    conected = True
    loged = False
    while conected:
        print('listing for messages....')
        if loged == False:
            message = connection.recv(1024).decode(Format)
<<<<<<< HEAD
            print(message, type(message))
            user_data = check_password_and_return_data(message)
            print(user_data)
            if user_data:
                User_data = user_data
                loged = True
                connection.send(
                    str({"user": user_data, "messages": Messages}).encode(Format))
=======
            user_data = check_password_and_return_data(message)
            if user_data:
                User_data = user_data
                loged = True
                connection.send(str(user_data).encode(Format))
>>>>>>> 84872b684fb5a8670f35b013e592646770a7c348
                Client = {
                    "user_id": user_data['temp_key'],
                    "connection": connection,
                    "address": address
                }
<<<<<<< HEAD
                print('after sending user data')
                Clients.append(Client)
        else:
            message = connection.recv(1024).decode(Format)
            message_object = save_message_to_kash(message, User_data)
            spredMessage(str(message_object))

            print('message recivevd....',  message, ' from addres: ', address)

            if message == DISCONECTED_MESSAGE:
                print('client disconacted')
                conected = False

=======
                Clients.append(Client)
        else:
            message = connection.recv(1024).decode(Format)

            spredMessage(message)
            save_message_to_db(message)
            print('message recivevd....',  message, ' from addres: ', address)
            if message == DISCONECTED_MESSAGE:
                print('client disconacted')
                conected = False
>>>>>>> 84872b684fb5a8670f35b013e592646770a7c348
    handle_disconect(connection, address, User_data['id'])
    #  connection.close()


<<<<<<< HEAD
def set_json1(file_name, users_data):
    with open(file_name, 'w') as outfile:
        return json.dump(users_data, outfile)


def server_script():
=======
def get_users(file_name):
    with open(file_name, 'r') as my_file:
        data = json.load(my_file)
        return data
>>>>>>> 84872b684fb5a8670f35b013e592646770a7c348


def set_users(file_name, users_data):
    with open(file_name, 'w') as outfile:
        return json.dump(users_data, outfile)


def server_script():
    Users = get_users('users.json')
    Server.listen()
<<<<<<< HEAD

    while True:
        try:
            print('Waiting for CONNECTIONS...')
            connection, address = Server.accept()
            new_thred = Thread(
                target=client_handler, args=(connection, address))
            new_thred.start()
            print('total conected users: ', active_count()-1)
        except Exception:
            print(Exception)
            break
    set_json1('db/messages.json', Messages)
    set_json1('db/users.json', Users)
=======

    while True:
        print('Waiting for CONNECTIONS...')
        connection, address = Server.accept()

        new_thred = Thread(
            target=client_handler, args=(connection, address))
        new_thred.start()
        print('total conected users: ', active_count()-1)
>>>>>>> 84872b684fb5a8670f35b013e592646770a7c348


if __name__ == "__main__":
    server_script()


# ריבוי משתמשים C
# פונקציה כללית של כתיבה לDB
# מ app.py להריץ שרת ו3 יוזרים ששולחים הודעות שונות
