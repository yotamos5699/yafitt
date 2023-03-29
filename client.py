from Socket import Socket
from tkinter import *
from tkinter.scrolledtext import *
ui = Tk()
my_text = ScrolledText(ui, height=40)
input_text = Entry(ui, width=10,)

# yafit a homohit


def get_prev_messages(user_id):

    return 'mock data is here'


def send_massege_button():
    pass
    # new_client.send()


def build_UI(user_name, user_id):
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


build_UI('yotam', '09127460920u6o0uieroyn')
ui.mainloop()

# new_client = Socket(5001, True).socket


# def send_massege(massege):
#     new_client.send(massege)


# send_massege("hi how are you".encode('utf-8'))


# while True:
#     pass
send_massege("hi how are you".encode('utf-8'))


while True:
    print(new_client.recv(1024).decode('utf-8'))
    pass
s
