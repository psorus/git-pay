import json
import os
from qtime import *
from betterhash import bhash as hash


class transaction(object):

    def __init__(s,fro,too,value,date=None):
        s.fro=fro
        s.too=too
        s.value=int(value)
        if date is None:date=now().q
        s.date=date

    def query(s):
        v=s.value
        v=int(v)
        if v<0:v=0
        return v


    def hash(s):
        return hash(s)

    def __str__(s):
        return f"{s.value}*{s.fro} => {s.too}"

    def __repr__(s):
        return str(s)

    def to_dict(s):
        return {"fro":s.fro,"too":s.too,"value":s.value,"date":s.date}

    def save(s):
        with open(f"../transactions/{s.hash()}.json","w") as f:
            f.write(json.dumps(json.dumps(s.to_dict(),indent=2)))

def transaction_from_dict(q):
    if type(q) is str:q=json.loads(q)
    return transaction(**q)

def load_transaction(q):
    #print("loading",q)
    with open(f"../transactions/"+q,"r") as f:
        return transaction_from_dict(json.loads(f.read()))

def load_transactions():
    ret=[]
    for fil in os.listdir("../transactions"):
        ret.append(load_transaction(fil))
    return ret


if __name__=="__main__":
    print(load_transactions())
