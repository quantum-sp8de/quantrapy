import base64

from .keys import EOSKey
from itertools import cycle


def xor_crypt_encode(data, key = 'AwesoMePassworD129'):
    '''
    data, key - str object
    return: str encoded object
    '''
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))

    return base64.b64encode(xored.encode()).decode()

def xor_crypt_decode(data, key = 'AwesoMePassworD129'):
    '''
    data, key - str object
    return: str decoded object
    '''
    data = base64.b64decode(data.encode()).decode()
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))

    return xored

def generate_dynamic_key():
    return EOSKey().to_public()

if __name__ == "__main__":
    print("===== Testing XOR =====")
    msg = "This is some interesting message. Hello! @#$"
    key = 'SuperPuperKey'
    e_msg = xor_crypt_encode(msg, key)
    print("Encrypted message: %s" % e_msg)
    msg_dec = xor_crypt_decode(e_msg, key)
    print("Decrypted message: %s" % msg_dec)
    print("Messages matches: %s" % (msg == msg_dec))

    print("===== Testing generating some dynanic keys ======")
    print("key 1: %s" % generate_dynamic_key())
    print("key 2: %s" % generate_dynamic_key())
    print("key 3: %s" % generate_dynamic_key())
    d_key = generate_dynamic_key()
    print("the len of dynamic key is 53: %s" % (53 == len(d_key)))
