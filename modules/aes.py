import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random


BLOCK_SIZE = 16
pad = lambda s: s + ((BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)).encode()
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def encrypt(raw, password):
    private_key = hashlib.sha256(password.encode()).digest()
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

def decrypt(enc, password):
    private_key = hashlib.sha256(password.encode()).digest()
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))

def enc(read, write, pwd):
    with open(read, "rb") as f:
        data = f.read()

    data = encrypt(data, pwd)

    with open(write, "wb") as f:
        f.write(data)

def dec(read, write, pwd):
    with open(read, "rb") as f:
        data = f.read()

    data = decrypt(data, pwd)

    with open(write, "wb") as f:
        f.write(data)
