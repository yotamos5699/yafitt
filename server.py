
from Socket import Socket
import random
from typing import TypedDict, Any
from datetime import datetime
import json
from threading import Thread, active_count
from cryptography.fernet import Fernet

from typingClasses import Client_, Message_, User_


DISCONECTED_MESSAGE = 'DISCONECTED'
Format = 'utf-8'


# לכתוב טייפ להודעה
# לטעון קובץ הודעות בתחילת הפונקציה המרכזית למשתנה
# לעדכן את המשתנה בהודעה חדשה כל פעם שמגיע כזאת
# לשמור הודעות לדאטה בייס בכל ניתוק לקוח או שרת

def get_json1(file_name):
    with open(file_name, 'r') as my_file:
        data = json.load(my_file)
        return data


Clients: list[Client_] = []
Users: list[User_] = get_json1('db/users.json')
Messages: list[Message_] = get_json1('db/messages.json')

Server = Socket(5001).socket


def castum_encrypt(message, key):
    fernet_suit = Fernet(str(key))
    return fernet_suit.encrypt(message)


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
    set_json1('messages.json', Messages)
    # delete client from Clients List based on the address


def check_password_and_return_data(password):

    for user in Users:
        if user['password'] == password:

            user['is_connected'] = True
            user['temp_key'] = random.randint(1, 50)
            user['connections'] = user['connections'] + 1
            return user
    return False


def client_handler(connection, address):

    connection.send(
        str({'msg': "ok"}).encode(Format))
    User_data = {}
    conected = True
    loged = False
    while conected:
        print('listing for messages....')
        if loged == False:
            message = connection.recv(1024).decode(Format)
            print(message, type(message))
            user_data = check_password_and_return_data(message)
            print(user_data)
            if user_data:
                User_data = user_data
                loged = True
                connection.send(
                    str({"user": user_data, "messages": Messages}).encode(Format))
                Client = {
                    "user_id": user_data['temp_key'],
                    "connection": connection,
                    "address": address
                }
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

    handle_disconect(connection, address, User_data['id'])
    #  connection.close()


def set_json1(file_name, users_data):
    with open(file_name, 'w') as outfile:
        return json.dump(users_data, outfile)


# def server_script():

#     # def set_users(file_name, users_data):
#     #     with open(file_name, 'w') as outfile:
#     #         return json.dump(users_data, outfile)


def server_script():
    # Users = get_users('users.jsony')
    Server.listen()

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


if __name__ == "__main__":
    server_script()


# ריבוי משתמשים C
# פונקציה כללית של כתיבה לDB
# מ app.py להריץ שרת ו3 יוזרים ששולחים הודעות שונות
