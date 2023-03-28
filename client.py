from Socket import Socket

new_client = Socket(5001, True).socket


def send_massege(massege):
    new_client.send(massege)


send_massege("hi how are you".encode('utf-8'))


while True:
    print(new_client.recv(1024).decode('utf-8'))
    pass
s