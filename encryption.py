from cryptography.fernet import Fernet


def castum_encrypt(message, key):
    fernet_suit = Fernet(str(key))
    return fernet_suit.encrypt(message)


def castum_decrypt(message, key):
    fernet_suit = Fernet(str(key))
    return fernet_suit.decrypt(message)
