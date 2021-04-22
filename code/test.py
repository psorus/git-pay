from transaction import *
from user import *

from extract_pk import extract_pk

ts=load_transactions()
us=load_users()

keys={zw.nam:extract_pk(zw.key) for zw in us}

print(keys)

for t in ts:
    print(t)
    print(t.to_dict())
    key=keys[t.fro]
    print(key)


