import base64
from cryptography.fernet import Fernet


def return_keys():
    keysHash = {}

    for i in range(1, 50):
        keysHash[i] = Fernet.generate_key()
    return keysHash


def castum_encrypt(message, key):
    print('in castum encrypt: ', message, key)

    fernet_suit = Fernet(key)
    return fernet_suit.encrypt(str(message).encode('utf-8'))


def castum_decrypt(message, key):
    print('key !!!:', key, type(key), 'message !!:', message, type(message))
    # m = message.decode('utf-8')
    # print(m, type(m))
    fernet_suit = Fernet(key)
    bytesResponse = fernet_suit.decrypt(message.encode('utf-8'))
    print('end of decrypt', bytesResponse, type(bytesResponse))
    return bytesResponse.decode('utf-8')


# keys = return_keys()


# message = 'hi how are u'


# enmsg = castum_encrypt(message, keys[1])
# print(enmsg)

# decmsg = castum_decrypt(enmsg, keys[1])
# print('dec message ', decmsg)
# enc_message = castum_decrypt(message, k)
# print(enc_message)
# dec_message = castum_decrypt(enc_message, keys[1])
# print(dec_message)
