import json
import os



class user(object):

    def __init__(s,nam,id,worth=0):#worth is always given in euro/100
        s.nam=nam
        s.id=id
        s.worth=int(worth)

    def __str__(s):
        return f"{s.nam}({s.id}):{s.worth}"
    def __repr__(s):
        return str(s)
    def to_dict(s):
        return {"nam":s.nam,"id":s.id,"worth":s.worth}

    def save(s):
        with open(f"../users/{s.nam}.json","w") as f:
            f.write(json.dumps(s.to_dict(),indent=2,sort_keys=True))



def user_from_dict(q):
    return user(**q)

def load_user(q):
    with open(f"../users/{q}.json","r") as f:
        return user_from_dict(json.loads(f.read()))


def load_users():
    ret=[]
    for fil in os.listdir("../users/"):
        if not ".json" in fil:continue
        fil=fil[:-5]
        ret.append(load_user(fil))
    return ret


if __name__=="__main__":
    print(load_users())



