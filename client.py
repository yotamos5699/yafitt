from Socket import Socket
from threading import Thread
from tkinter import *
from tkinter.scrolledtext import *


def handle_login():
    pass


ui = Tk()
login = Tk()
my_label1 = Label(login, text="insert password:").pack()
input_password = Entry(login, width=10).pack()
login_btn = Button(login, text="login", command=handle_login).pack()
my_text = ScrolledText(ui, height=40)
input_text = Entry(ui, width=10)
is_loged = False
# new_client = Socket(5001, True).socket


# //


def get_prev_messages(user_id):

    return 'mock data is here'


def send_massege_button():
    pass
    # new_client.send()


def build_chat(user_name, user_id):
    # ui.geometry()
    ui.title(user_name+"Chat:")
    my_label = Label(ui, text="Chat:")
    my_label.pack()
    my_text.insert(END, get_prev_messages(user_id))
    my_text.pack()

    my_text.pack()
    my_text.focus()
    my_btn = Button(ui, text="Send Message:", command=send_massege_button)
    my_label_2 = Label(ui, text="Message:", height=3)
    my_label_2.pack()
    input_text.pack()
    my_btn.pack(padx=10, pady=10)


def build_UI():
    while True:
        if (is_loged):
            build_chat('yotam', '23234574')
            ui.mainloop()
        else:
            login.mainloop()


# def send_massege(massege):
#     new_client.send(massege)


# send_massege("hi how are you".encode('utf-8'))


# def client_script():
#     send_massege("hi i'm connected".encode('utf-8'))
#     while True:
#         print(new_client.recv(1024).decode('utf-8'))


def run_client():
    # ClientScript = Thread(target=client_script)
    ClientUi = Thread(target=build_UI)
    ClientUi.start()
    # ClientScript.start()


run_client()
