from datetime import datetime,timedelta
from qtime import *

import os
from transaction import transaction


def times():

    t0=datetime(2021,1,1)
    t1=datetime(2121,1,1)
    
    y,m,d=2021,1,1
    maxy=2121

    while y<maxy:
        yield qtime(datetime(y,m,d)).q
        m+=1
        if m>12:
            m=1
            y+=1

def erbsunde(fro,too,value,sk,saveas):
    bp=f"../transactions/{saveas}/"
    os.makedirs(bp,exist_ok=False)
    for date in times():
        t=transaction(fro,too,value,date=date)
        t.signate(sk)
        t.save(bp+str(date)+".json")
    




if __name__=="__main__":
    from gen_keys import gen_keys
    sk,pk,opk=gen_keys("either collect crash clump twelve verb front affair parrot despair term asset")
    erbsunde("dummy","dummy2",1,sk,"testsünde")    














