from transaction import *
from user import *

from extract_pk import extract_pk

from qtime import now


def calculate():
    u=load_users()
    t=load_transactions()

    inv=0
    
    #against sundenattack
    hashs=[zw.hash() for zw in t]
    if len(list(set(hashs)))!=len(hashs):
        for i1,h1 in enumerate(hashs):
            for i2,h2 in enumerate(hashs):
                if i2<=i1:continue
                if h1==h2:
                    print("duplicate",h1)
        inv=1
        print("found duplicate")


    q={zw.nam:zw.worth for zw in u}
    keys={zw.nam:extract_pk(zw.key) for zw in u}


    time=now().q

    for tt in t:
        if not tt.fro in q.keys():
            inv+=1
            print("found wrong fro",tt.hash()) 
            continue    
        if not tt.too in q.keys():
            inv+=1
            print("found wrong too",tt.hash()) 
            continue
        if tt.date>time:continue
        key=keys[tt.fro]
        if not tt.verify(key):
            print("found unverfiable",tt.hash()) 
            inv+=1
            continue
        ac=tt.query()
        q[tt.fro]-=ac
        q[tt.too]+=ac

    return inv,q

if __name__=="__main__":
    inv,q=calculate()
    print(inv)
    print(json.dumps(q))

