import secrets


def gen(len, chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890123456789!#$%*+,-./:;<=>?@_"):
    pwd = ""
    for i in range(len):
        pwd += secrets.choice(chars)
    return pwd
