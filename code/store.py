from aes import encrypt,decrypt

import os
import json


def fnam(nam):
    return f"../store/{nam}.json"

def has_store(nam):
    return os.path.isfile(fnam(nam))

def save_store(nam,mne,pwd):
    ciph,tag,nonce=encrypt(mne,pwd)
    with open(fnam(nam),"w") as f:
        f.write(json.dumps({"ciph":ciph,"tag":tag,"nonce":nonce},indent=2))

def load_store(nam,pwd):
    with open(fnam(nam),"r") as f:
        q=json.loads(f.read())
    ciph=q["ciph"]
    tag=q["tag"]
    nonce=q["nonce"]

    mne,val=decrypt(ciph,tag,nonce,pwd)
    return mne,val



