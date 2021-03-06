import json
import os
from qtime import *
from betterhash import bhash as hash


class transaction(object):

    def __init__(s,fro,too,value,date=None,sign=None):
        s.fro=fro
        s.too=too
        s.value=int(value)
        if date is None:date=now().q
        s.date=date
        s.sign=sign

    def query(s):
        v=s.value
        v=int(v)
        if v<0:v=0
        return v


    def hash(s):
        return hash(json.dumps(s.to_dict(),indent=2,sort_keys=True))

    def __str__(s):
        return f"{s.value}*{s.fro} => {s.too}"

    def __repr__(s):
        return str(s)

    def to_dict(s):
        return {"fro":s.fro,"too":s.too,"value":s.value,"date":s.date,"sign":s.sign}
    def small_dict(s):
        """to_dict without signature (used to calculate this signature)"""
        return {"fro":s.fro,"too":s.too,"value":s.value,"date":s.date}
    def _signbytes(s):
        return json.dumps(s.small_dict(),indent=2,sort_keys=True).encode()
    def signate(s,sk):
        s.sign=sk.sign(s._signbytes()).hex()
        #s.sign=sk.sign(json.dumps(s.small_dict(),indent=2,sort_keys=True).encode())
    def verify(s,pk):
        return pk.verify(bytes.fromhex(s.sign),s._signbytes())
    def save(s,fn=None):
        if fn is None:
            fn=f"../transactions/{s.hash()}.json"

        with open(fn,"w") as f:
            f.write(json.dumps(s.to_dict(),indent=2))
    def save_no_overwride(s):
        #fn=f"../users/{s.nam}.json"
        fn=f"../transactions/{s.hash()}.json"
        if os.path.isfile(fn):raise Exception("This already exists")
        with open(fn,"w") as f:
            f.write(json.dumps(s.to_dict(),indent=2))

def transaction_from_dict(q):
    if type(q) is str:q=json.loads(q)
    return transaction(**q)

def load_transaction(q):
    #print("loading",q)
    with open(f"../transactions/"+q,"r") as f:
        return transaction_from_dict(json.loads(f.read()))

def bistdir(pth):
    """os.listdir but recursive"""

    if len(pth)>0 and not pth[-1]=="/":
        pth=pth+"/"

    ret=[]

    for fn in os.listdir(pth):
        fn=pth+fn
        if os.path.isfile(fn):
            ret.append(fn)
        else:
            for zw in bistdir(fn):
                ret.append(zw)

    return ret



def load_transactions():
    ret=[]
    for fil in bistdir("../transactions/"):
        fil=fil[16:]#bad code to extend to work with subfolders
        #print(fil)
        #exit()
        ret.append(load_transaction(fil))
    return ret


if __name__=="__main__":
    print(load_transactions())
