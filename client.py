from typing import Any, TypedDict
from Socket import Socket
from threading import Thread
from tkinter import *
from tkinter.scrolledtext import *
import json
import time
from cryptography.fernet import Fernet

from typingClasses import Message_, User_


def get_json1(file_name):
    with open(file_name, 'r') as my_file:
        data = json.load(my_file)
        return data


def set_json1(file_name, users_data):
    with open(file_name, 'w') as outfile:
        return json.dump(users_data, outfile)


def castum_decrypt(message, key):
    fernet_suit = Fernet(str(key))
    return fernet_suit.decrypt(message)


new_client = Socket(5001, True).socket


# להתחבר עם 2 יוזרים שונים לבדוק שיש מעבר בין מסכים תקין
# להכניס הודעות דמה לקובץ ולוודא שנמשכות הודעות כמו שצריך


def send_massege_button():
    send_massege(input_text.get().encode('utf-8'))


def send_massege(massege):
    new_client.send(massege)


def run_ui():
    master_ui = Tk()
    chat_ui = Frame(master_ui)
    login_ui = Frame(master_ui)

    def handle_login():
        message = input_password.get()
        print('password: ', message)
        send_massege(input_password.get().encode('utf-8'))
        time.sleep(2)
        data = eval(get_json1('db/client_cash.json'))

        print('data in hndle login !!', data, type(data))
        if data == False:

            # להציג הודעה שהלקוח לא קיים
            return
        else:
            user: User_ = data['user']
            messages = data['messages']

            if user['connections'] > 1:
                # להציג הודעה שהלקוח כבר מחובר ממקום אחר
                return
            print('set chat ui')
            login_ui.pack_forget()
            master_ui.title(user['user_name']+"Chat:")
            my_label = Label(chat_ui, text="Chat:")
            my_label.pack()
            my_text.insert(END, messages)
            my_text.pack()
            chat_ui.pack()

    global input_password
    input_password = Entry(login_ui, width=10)
    my_label1 = Label(login_ui, text="insert password:").pack()

    input_password.pack()
    login_btn = Button(login_ui, text="login", command=handle_login)
    login_btn.pack()
    global my_text
    my_text = ScrolledText(chat_ui, height=40)
    global input_text
    input_text = Entry(chat_ui, width=10)

    login_ui.pack()

    my_label = Label(chat_ui, text="Chat:")
    my_label.pack()

    my_text.pack()
    my_text.focus()
    my_btn = Button(chat_ui, text="Send Message:", command=send_massege_button)
    my_label_2 = Label(chat_ui, text="Message:", height=3)
    my_label_2.pack()
    input_text.pack()
    my_btn.pack(padx=10, pady=10)
    master_ui.mainloop()


def run_main_loop():

    c = Thread(target=client_script)
    u = Thread(target=run_ui)
    u.start()
    c.start()


# https: // github.com/yotamos5699/yafitt.git
# send_massege("hi how are you".encode('utf-8'))


def client_script():
    messagesCounter = 0
    User = None
    # Thread(target=run_main_loop).start()
    print('client script')
    while True:
        print('in client script')
        result = new_client.recv(1024).decode('utf-8')
        print('got answer', result, 'user ', User,
              'messagesCounter: ', messagesCounter)

        if result and User == None and messagesCounter != 0:
            print('result and user none', type(result))
            data = eval(result)
            print(data, type(data))
            User: User_ = data['user']
            set_json1('db/client_cash.json', result)
            Messages: list[Message_] = data['messages']

            print('user: ', User)
            print('messages: ', Messages)

        elif messagesCounter != 0:
            decrypted_message: Message_ = json.load(
                castum_decrypt(result, User["temp_key"]))
            my_text.insert(
                END, decrypted_message["time_stemp"]+" " + User["user_name"]+':'+decrypted_message["message"])
        messagesCounter += 1


if __name__ == "__main__":
    run_main_loop()
