from typing import Any, TypedDict
from Socket import Socket
from threading import Thread
from tkinter import *
from tkinter.scrolledtext import *
import json
new_client = Socket(5001, True).socket


def handle_login():
    send_massege(input_password.get().encode('utf-8'))


master_ui = Tk()
chat_ui = Frame(master_ui)

login_ui = Frame(master_ui)
my_label1 = Label(login_ui, text="insert password:").pack()
input_password = Entry(login_ui, width=10)
input_password.pack()
login_btn = Button(login_ui, text="login", command=handle_login).pack()
my_text = ScrolledText(chat_ui, height=40)
input_text = Entry(chat_ui, width=10)
is_loged = False


# //


def get_prev_messages(user_id):

    return 'mock data is here'


# def send_massege_button():
#     pass
    # new_client.send()

    # ui.geometry()
# chat_ui.title(user_name+"Chat:")
my_label = Label(chat_ui, text="Chat:")
my_label.pack()
# my_text.insert(END, get_prev_messages(user_id))
# my_text.pack()

my_text.pack()
my_text.focus()
my_btn = Button(chat_ui, text="Send Message:", command=send_massege_button)
my_label_2 = Label(chat_ui, text="Message:", height=3)
my_label_2.pack()
input_text.pack()
my_btn.pack(padx=10, pady=10)


def send_massege(massege):
    new_client.send(massege)


send_massege("hi how are you".encode('utf-8'))


def client_script():
    User = None
    login_ui.pack()
    master_ui.mainloop()

    while True:
        result = new_client.recv(1024).decode('utf-8')
        if result and User == None:
            User = json.load(result)
            login_ui.pack_forget()
            chat_ui.title(User['user_name']+"Chat:")
            my_label = Label(chat_ui, text="Chat:")
            my_label.pack()
            my_text.insert(END, get_prev_messages(User['id']))
            my_text.pack()
            chat_ui.pack()


# def run_client():
#     ClientScript = Thread(target=client_script)
#     # ClientUi = Thread(target=build_UI)
#     # ClientUi.start()
#     ClientScript.start()


# run_client()
