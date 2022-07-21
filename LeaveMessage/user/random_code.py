import random
import string

def make_code():
    _LENGTH = 8

    string_pool = string.ascii_letters + string.digits

    result = ""

    for i in range(_LENGTH):
        result += random.choice(string_pool)

    return result