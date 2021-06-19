from Crypto.Cipher import AES


def keymod(key):
    key+="".join(["0"*16])
    key=key[:16]
    return key


def encrypt(data,key):

    key=keymod(key)
    data=data.encode("utf8")
    key=key.encode("utf8")
    cipher = AES.new(key, AES.MODE_EAX)

    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)


    ciphertext=ciphertext.hex()
    tag=tag.hex()
    nonce=nonce.hex()

    return ciphertext,tag,nonce


def decrypt(ciphertext,tag,nonce,key):
    key=keymod(key)
    key=key.encode("utf8")
    ciphertext=bytes.fromhex(ciphertext)
    tag=bytes.fromhex(tag)
    nonce=bytes.fromhex(nonce)

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)
    try:
        cipher.verify(tag)
        valid=True
    except ValueError:
        valid=False

    plaintext=plaintext.decode("utf8")

    return plaintext,valid


if __name__=="__main__":
    tex="Hello World"
    key="1234"
    ciph,tag,nonce=encrypt(tex,key)
    rtex,val=decrypt(ciph,tag,nonce,key)
    print(rtex,val)



