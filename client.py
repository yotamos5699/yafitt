from typing import Any, TypedDict
from Socket import Socket
from threading import Thread
from tkinter import *
from tkinter.scrolledtext import *

import json
import time
from cryptography.fernet import Fernet
from encrypt import castum_decrypt
import datetime
from typingClasses import Message_, User_
DISCONECTED_MESSAGE = 'DISCONECTED'


def get_json1(file_name):
    with open(file_name, 'r') as my_file:
        data = json.load(my_file)
        return data


def set_json1(file_name, users_data):
    with open(file_name, 'w') as outfile:
        return json.dump(users_data, outfile)


new_client = Socket(5001, True).socket


# להתחבר עם 2 יוזרים שונים לבדוק שיש מעבר בין מסכים תקין
# להכניס הודעות דמה לקובץ ולוודא שנמשכות הודעות כמו שצריך


def send_massege_button():
    send_massege(input_text.get().encode('utf-8'))


def send_massege(massege):

    new_client.send(massege)


global isDisconected


def handle_window_close():
    print('in handle close...')
    new_client.send(DISCONECTED_MESSAGE.encode('utf-8'))
    new_client.shutdown(2)
    new_client.close()
    master_ui.destroy()


def run_ui():
    global master_ui
    master_ui = Tk()
    global ErrorBox

    chat_ui = Frame(master_ui)
    login_ui = Frame(master_ui)
    ErrorBox = Text(login_ui, height=2, width=10)

    master_ui.protocol("WM_DELETE_WINDOW",  handle_window_close)

    def handle_login():

        message = input_password.get()
        send_massege(input_password.get().encode('utf-8'))
        time.sleep(2)
        data = eval(get_json1('db/client_cash.json'))

        print('data in hndle login !!', data, type(data))

        if "status" in data:
            ErrorBox.insert(END, "no data")
            ErrorBox.pack()
            # להציג הודעה שהלקוח לא קיים
            return
        else:

            user: User_ = data['user']
            messages = data['messages']

            if user['connections'] > 1:
                ErrorBox.insert(
                    END, 'already connected !!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                ErrorBox.pack()
                print('already connected !!!!!!!!!!!!!!!!!!!!!!!!!!!!')

                # להציג הודעה שהלקוח כבר מחובר ממקום אחר
                return
            print('set chat ui')
            login_ui.pack_forget()
            master_ui.title(user['user_name']+"Chat:")
            my_label = Label(chat_ui, text="Chat:")
            my_label.pack()

            formatedMessages = ""
            for message in messages:
                owner = "ME" if user['user_name'] == message["sender"] else message['sender']
                print(message, owner, 'user: ',
                      user['user_name'], 'sender: ', message['sender'])
                formatedMessages += str(message["time_stemp"] +
                                        " " + owner + ":" + message["message"] + "\n")
                # formatedMessages += str(message) + '\n'

            my_text.insert(END, formatedMessages)
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
    my_btn = Button(chat_ui, text="Send Message:",
                    command=send_massege_button)
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
        try:
            result = new_client.recv(2048).decode('utf-8')
        except:

            break
        print('got answer', result, 'user ', User,
              'messagesCounter: ', messagesCounter)
        set_json1('db/client_cash.json', "{'status':False}")
        if result and User == None and messagesCounter != 0:
            data = eval(result)
            User: User_ = data['user']
            set_json1('db/client_cash.json', result)
            Messages: list[Message_] = data['messages']

        elif messagesCounter != 0:

            decrypted_message: Message_ = eval(castum_decrypt(
                result, User["temp_key"]))
            owner = "ME" if User['user_name'] == decrypted_message["sender"] else decrypted_message['sender']
            my_text.insert(
                END, str(decrypted_message["time_stemp"])+" " + owner + ':'+decrypted_message["message"]+"\n")
        messagesCounter += 1


if __name__ == "__main__":
    run_main_loop()
