from transaction import *
from user import *

from extract_pk import extract_pk


def calculate():
    u=load_users()
    t=load_transactions()
    
    q={zw.nam:zw.worth for zw in u}
    keys={zw.nam:extract_pk(zw.key) for zw in u}

    inv=0

    for tt in t:
        if not tt.fro in q.keys():
            inv+=1
            continue    
        if not tt.too in q.keys():
            inv+=1
            continue
        key=keys[tt.fro]
        #if not tt.verify(key):
        #    inv+=1
        #    continue
        ac=tt.query()
        q[tt.fro]-=ac
        q[tt.too]+=ac

    return inv,q

if __name__=="__main__":
    inv,q=calculate()
    print(inv)
    print(json.dumps(q))

